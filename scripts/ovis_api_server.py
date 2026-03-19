import argparse
import base64
import io
import os
import time
from typing import Any, Dict, List, Optional

import requests
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from PIL import Image
from transformers import AutoModelForCausalLM
import uvicorn


MODEL_PATH = os.getenv("OVIS_MODEL_PATH", "AIDC-AI/Ovis2.5-9B")
DEFAULT_MAX_TOKENS = int(os.getenv("OVIS_MAX_TOKENS", "2048"))
DEFAULT_TEMPERATURE = float(os.getenv("OVIS_TEMPERATURE", "0.1"))
ENABLE_THINKING = os.getenv("OVIS_ENABLE_THINKING", "false").lower() == "true"
ENABLE_THINKING_BUDGET = os.getenv("OVIS_ENABLE_THINKING_BUDGET", "false").lower() == "true"
THINKING_BUDGET = int(os.getenv("OVIS_THINKING_BUDGET", "1024"))
USE_FAST_PROCESSOR = os.getenv("OVIS_USE_FAST_PROCESSOR", "true").lower() == "true"
ATTN_IMPLEMENTATION = os.getenv("OVIS_ATTN_IMPLEMENTATION", "sdpa")


device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" else torch.float32

if device == "cuda":
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    torch.backends.cudnn.benchmark = True
    torch.set_float32_matmul_precision("high")

print(f"[OVIS API] Loading model: {MODEL_PATH}")
print(f"[OVIS API] Device: {device}, dtype: {dtype}")
model_kwargs = {
    "torch_dtype": dtype,
    "trust_remote_code": True,
    "use_fast": USE_FAST_PROCESSOR,
}
if device == "cuda":
    model_kwargs["attn_implementation"] = ATTN_IMPLEMENTATION

effective_attn_implementation = model_kwargs.get("attn_implementation", "default")

try:
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        **model_kwargs,
    )
except TypeError:
    model_kwargs.pop("use_fast", None)
    try:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            **model_kwargs,
        )
        effective_attn_implementation = model_kwargs.get("attn_implementation", "default")
    except ValueError as exc:
        err = str(exc).lower()
        if "does not support an attention implementation" in err or "scaled_dot_product_attention" in err:
            model_kwargs["attn_implementation"] = "eager"
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_PATH,
                **model_kwargs,
            )
            effective_attn_implementation = "eager"
        else:
            raise
except ValueError as exc:
    err = str(exc).lower()
    if "does not support an attention implementation" in err or "scaled_dot_product_attention" in err:
        model_kwargs["attn_implementation"] = "eager"
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            **model_kwargs,
        )
        effective_attn_implementation = "eager"
    else:
        raise
if device == "cuda":
    model = model.cuda()
model.eval()
print(f"[OVIS API] Attention implementation: {effective_attn_implementation}")
print("[OVIS API] Model ready")


class ImageUrl(BaseModel):
    url: str


class ContentPart(BaseModel):
    type: str
    text: Optional[str] = None
    image_url: Optional[ImageUrl] = None


class Message(BaseModel):
    role: str
    content: Any


class ChatCompletionsRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = Field(default=DEFAULT_MAX_TOKENS)
    temperature: Optional[float] = Field(default=DEFAULT_TEMPERATURE)
    stream: Optional[bool] = False
    enable_thinking: Optional[bool] = None
    enable_thinking_budget: Optional[bool] = None
    thinking_budget: Optional[int] = None


app = FastAPI(title="OVIS OpenAI-Compatible API", version="1.0.0")


def load_image_from_data_url(url: str) -> Image.Image:
    if not url.startswith("data:image/"):
        raise ValueError("Only data URL images are supported: data:image/...;base64,...")

    try:
        _, encoded = url.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return image
    except Exception as exc:
        raise ValueError(f"Failed to decode data URL image: {exc}") from exc


def load_image_from_http_url(url: str, timeout: int = 30) -> Image.Image:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content)).convert("RGB")
        return image
    except Exception as exc:
        raise ValueError(f"Failed to fetch image URL: {exc}") from exc


def parse_openai_message_content(messages: List[Message]) -> tuple[str, Optional[Image.Image]]:
    prompt_parts: List[str] = []
    image: Optional[Image.Image] = None

    for message in messages:
        content = message.content

        if isinstance(content, str):
            if message.role == "user":
                prompt_parts.append(content)
            continue

        if isinstance(content, list):
            for part in content:
                part_type = part.type if isinstance(part, ContentPart) else part.get("type")

                if part_type == "text":
                    text = part.text if isinstance(part, ContentPart) else part.get("text", "")
                    if text:
                        prompt_parts.append(text)

                elif part_type == "image_url":
                    image_url_obj = part.image_url if isinstance(part, ContentPart) else part.get("image_url")
                    if not image_url_obj:
                        continue

                    url = image_url_obj.url if isinstance(image_url_obj, ImageUrl) else image_url_obj.get("url")
                    if not url:
                        continue

                    if url.startswith("data:image/"):
                        image = load_image_from_data_url(url)
                    elif url.startswith("http://") or url.startswith("https://"):
                        image = load_image_from_http_url(url)
                    else:
                        raise ValueError("Unsupported image_url format")

    prompt = "\n".join(prompt_parts).strip()
    return prompt, image


def run_ovis_inference(
    prompt: str,
    image: Optional[Image.Image],
    max_tokens: int,
    temperature: float,
    enable_thinking: Optional[bool] = None,
    enable_thinking_budget: Optional[bool] = None,
    thinking_budget: Optional[int] = None,
) -> str:
    if not prompt:
        raise ValueError("No prompt text provided")

    thinking_enabled = ENABLE_THINKING if enable_thinking is None else enable_thinking
    thinking_budget_enabled = (
        ENABLE_THINKING_BUDGET if enable_thinking_budget is None else enable_thinking_budget
    )
    requested_thinking_budget = THINKING_BUDGET if thinking_budget is None else thinking_budget

    content_parts: List[Dict[str, Any]] = []
    if image is not None:
        content_parts.append({"type": "image", "image": image})
    content_parts.append({"type": "text", "text": prompt})

    messages = [{"role": "user", "content": content_parts}]

    input_ids, pixel_values, grid_thws = model.preprocess_inputs(
        messages=messages,
        add_generation_prompt=True,
        enable_thinking=thinking_enabled,
    )

    if device == "cuda":
        input_ids = input_ids.cuda()
        pixel_values = pixel_values.cuda() if pixel_values is not None else None
        grid_thws = grid_thws.cuda() if grid_thws is not None else None

    generation_kwargs = {
        "inputs": input_ids,
        "pixel_values": pixel_values,
        "grid_thws": grid_thws,
        "enable_thinking": thinking_enabled,
        "enable_thinking_budget": thinking_budget_enabled,
        "max_new_tokens": max_tokens,
        "temperature": temperature,
    }

    if thinking_enabled and thinking_budget_enabled:
        generation_kwargs["thinking_budget"] = min(requested_thinking_budget, max(0, max_tokens - 25))

    with torch.inference_mode():
        outputs = model.generate(**generation_kwargs)

    prompt_token_len = input_ids.shape[-1]
    generated_tokens = outputs[0][prompt_token_len:]
    if generated_tokens.numel() == 0:
        generated_tokens = outputs[0]

    response_text = model.text_tokenizer.decode(generated_tokens, skip_special_tokens=True)
    return response_text


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/models")
def list_models() -> Dict[str, Any]:
    return {
        "object": "list",
        "data": [
            {
                "id": MODEL_PATH,
                "object": "model",
                "owned_by": "self-hosted",
            }
        ],
    }


@app.post("/v1/chat/completions")
def chat_completions(req: ChatCompletionsRequest) -> Dict[str, Any]:
    if req.stream:
        raise HTTPException(status_code=400, detail="stream=true not implemented in this server")

    try:
        prompt, image = parse_openai_message_content(req.messages)
        max_tokens = req.max_tokens or DEFAULT_MAX_TOKENS
        temperature = req.temperature if req.temperature is not None else DEFAULT_TEMPERATURE

        response_text = run_ovis_inference(
            prompt=prompt,
            image=image,
            max_tokens=max_tokens,
            temperature=temperature,
            enable_thinking=req.enable_thinking,
            enable_thinking_budget=req.enable_thinking_budget,
            thinking_budget=req.thinking_budget,
        )

        return {
            "id": "chatcmpl-ovis-local",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": MODEL_PATH,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text,
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OVIS OpenAI-compatible API server")
    parser.add_argument("--host", default=os.getenv("OVIS_API_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("OVIS_API_PORT", "8000")))
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
