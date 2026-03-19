import base64
import json
import os
import sys
import tempfile
from pathlib import Path

import requests
from PIL import Image, ImageOps


def preprocess_image(doc_path: Path) -> bytes:
    """Preprocess PDF/image for Llama Vision.
    
    Args:
        doc_path: Path to document (PDF or image).
    
    Returns:
        Preprocessed image data as bytes (PNG format).
    """
    max_width, max_height = 1024, 1024

    if doc_path.suffix.lower() == ".pdf":
        try:
            import pdf2image
            print(f"Converting PDF to image: {doc_path}", flush=True)
            images = pdf2image.convert_from_path(str(doc_path), first_page=1, last_page=1, dpi=200)
            if not images:
                raise RuntimeError("Failed to convert PDF to images")
            image = images[0]
        except Exception as e:
            print(f"\nERROR: PDF conversion failed: {e}")
            print("\nTo convert PDFs on Windows, install poppler:")
            print("  1. Download from: https://github.com/oschwalde/poppler-windows/releases/")
            print("  2. Extract and add bin/ folder to PATH")
            print("\nAlternative: Convert PDF to PNG first, then update invoice_path in this script.")
            raise
    else:
        image = Image.open(doc_path)

    # Optimize for vision model
    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)

    # Save to bytes
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        image.save(tmp.name, "PNG", optimize=True)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            image_data = f.read()
    finally:
        os.unlink(tmp_path)

    return image_data


def resolve_endpoints() -> list[str]:
    in_container = Path("/.dockerenv").exists()
    default_endpoint = "http://host.docker.internal:11434/api/generate" if in_container else "http://localhost:11434/api/generate"
    fallback_endpoint = "http://localhost:11434/api/generate" if in_container else "http://host.docker.internal:11434/api/generate"
    return [os.getenv("OLLAMA_GENERATE_URL", default_endpoint), fallback_endpoint]


def get_available_models(endpoints: list[str]) -> set[str]:
    tags_endpoints = []
    for generate_url in endpoints:
        base_url = generate_url.replace("/api/generate", "")
        tags_endpoints.append(f"{base_url}/api/tags")

    for tags_url in tags_endpoints:
        try:
            response = requests.get(tags_url, timeout=(5, 20))
            if response.status_code != 200:
                continue

            payload = response.json()
            return {model.get("name", "") for model in payload.get("models", []) if model.get("name")}
        except requests.exceptions.RequestException:
            continue

    return set()


def choose_structuring_model(available_models: set[str]) -> str:
    preferred = os.getenv("STRUCTURING_MODEL", "llama3.2:3b")
    if preferred in available_models:
        return preferred

    for candidate in ["llama3.2:3b", "llama3.2-vision:11b"]:
        if candidate in available_models:
            print(f"[STAGE_2_LLAMA_STRUCT] Preferred model '{preferred}' not found. Falling back to '{candidate}'.")
            return candidate

    return preferred


def stream_ollama_call(endpoints: list[str], payload: dict, stage_name: str) -> str:
    last_error = None

    for endpoint in endpoints:
        try:
            print(f"[{stage_name}] Calling endpoint: {endpoint}", flush=True)
            response = requests.post(endpoint, json=payload, timeout=(5, 600), stream=True)

            if response.status_code != 200:
                print(f"[{stage_name}] ERROR: HTTP {response.status_code}: {response.text}")
                last_error = RuntimeError(f"HTTP {response.status_code}")
                continue

            full_text = ""
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue

                if isinstance(line, bytes):
                    line = line.decode("utf-8", errors="ignore")

                try:
                    parsed_line = json.loads(line)
                    full_text += parsed_line.get("response", "")
                    if parsed_line.get("done"):
                        break
                except json.JSONDecodeError:
                    pass

            print(f"[{stage_name}] Complete", flush=True)
            return full_text.strip()
        except requests.exceptions.Timeout as exc:
            last_error = exc
            print(
                f"[{stage_name}] Request timed out on {endpoint}: {exc}. "
                "Increase timeout or retry after model warm-up.",
                flush=True,
            )
        except requests.exceptions.RequestException as exc:
            last_error = exc
            print(f"[{stage_name}] Request failed on {endpoint}: {exc}", flush=True)

    raise RuntimeError(f"[{stage_name}] Failed on all endpoints. Last error: {last_error}")


def extract_json_block(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end != -1 and end > start:
        return stripped[start : end + 1]
    return stripped


def main() -> None:
    # Hardcoded test invoice path
    # For Windows host: use r"D:\Documents\0124.pdf"
    # For Docker container: use "/tmp/0124.pdf"
    in_container = Path("/.dockerenv").exists()
    invoice_path = Path("/tmp/0124.pdf") if in_container else Path(r"D:\Documents\0124.pdf")
    
    if not invoice_path.exists():
        print(f"ERROR: Invoice not found at {invoice_path}")
        sys.exit(1)

    # Preprocess image
    print("Preprocessing invoice image...", flush=True)
    image_data = preprocess_image(invoice_path)
    b64_image = base64.b64encode(image_data).decode("ascii")
    print(f"Encoded image: {len(b64_image)} chars", flush=True)

    endpoints = resolve_endpoints()
    available_models = get_available_models(endpoints)

    # Stage 1: GLM-OCR extraction in two passes (full text + table)
    glm_model = os.getenv("GLM_OCR_MODEL", "glm-ocr:latest")

    text_prompt = """Text Recognition: 
Extract all text from this invoice and return in Markdown, omiting any content in table format.
Preserve reading order, emphasize structures like bolding, headers, and section/grouping as much as possible.
Return only Markdown."""

    table_prompt = """Table Recognition:
Extract all data in table format into Markdown table format.
Return only Markdown."""

    stage1_text_payload = {
        "model": glm_model,
        "prompt": text_prompt,
        "images": [b64_image],
        "stream": True,
        "temperature": 0.0,
    }

    stage1_table_payload = {
        "model": glm_model,
        "prompt": table_prompt,
        "images": [b64_image],
        "stream": True,
        "temperature": 0.0,
    }

    text_markdown = stream_ollama_call(endpoints, stage1_text_payload, stage_name="STAGE_1_GLM_TEXT")
    print("MARKDOWN_OUTPUT_START_text")
    print(text_markdown.strip())
    print("MARKDOWN_OUTPUT_END_text")
    table_markdown = stream_ollama_call(endpoints, stage1_table_payload, stage_name="STAGE_1_GLM_TABLE")
    print("MARKDOWN_OUTPUT_START_table")
    print(table_markdown.strip())
    print("MARKDOWN_OUTPUT_END_table")

    markdown_text = (
        "## OCR_TEXT\n"
        f"{text_markdown.strip()}"
        "## OCR_TABLE\n"
        f"{table_markdown.strip()}"
    ).strip()

    if not markdown_text:
        print("[STAGE_1_GLM_OCR] Empty markdown output after text+table passes")
        sys.exit(1)

#    print("MARKDOWN_OUTPUT_START")
#    print(markdown_text)
#    print("MARKDOWN_OUTPUT_END")

    # Stage 2: Llama text model creates structured JSON from markdown
    stage2_prompt = f"""You are an invoice data extraction system that returns ONLY valid JSON.

Task: Read the OCR markdown below and extract ALL data into the exact JSON structure shown.

DO NOT write code. DO NOT write explanations. DO NOT use markdown code blocks.
ONLY return the filled JSON object with extracted values.

Required JSON structure:
{{
  "vendor_details": {{
    "vendor_name": "",
    "vendor_address": "",
    "vendor_gst_no": "",
    "vendor_mobile_no_1": "",
    "vendor_mobile_no_2": "",
    "email_id": "",
    "vendor_signature": "",
    "agent_broker_name": ""
  }},
  "bill_details": {{
    "bill_date": "",
    "bill_no": "",
    "bill_type": "",
    "bill_to": "",
    "po_no": "",
    "eway_bill_no": "",
    "acknowledge_no": ""
  }},
  "transport_details": {{
    "vehicle_no": "",
    "driver_name": "",
    "driver_no": ""
  }},
  "bank_details": {{
    "account_holder_name": "",
    "account_number": "",
    "ifsc_code": ""
  }},
  "items": [
    {{
      "item_no": "",
      "item_name": "",
      "hsn_code": "",
      "gst_percent": "",
      "uom": "",
      "quantity": "",
      "rate": "",
      "amount": ""
    }},
    {{
      "item_no": "",
      "item_name": "",
      "hsn_code": "",
      "gst_percent": "",
      "uom": "",
      "quantity": "",
      "rate": "",
      "amount": ""
    }},
    {{
      "item_no": "",
      "item_name": "",
      "hsn_code": "",
      "gst_percent": "",
      "uom": "",
      "quantity": "",
      "rate": "",
      "amount": ""
    }},
    {{
      "item_no": "",
      "item_name": "",
      "hsn_code": "",
      "gst_percent": "",
      "uom": "",
      "quantity": "",
      "rate": "",
      "amount": ""
    }},
    {{
      "item_no": "",
      "item_name": "",
      "hsn_code": "",
      "gst_percent": "",
      "uom": "",
      "quantity": "",
      "rate": "",
      "amount": ""
    }}
  ]
}}

Rules:
- Extract data from the markdown into the JSON structure above
- Use EXACTLY these field names: vendor_details, bill_details, transport_details, bank_details, items
- Fill in values from the markdown below, use empty string "" for missing fields
- Return ONLY the JSON object, no code, no explanations, no markdown formatting

OCR Markdown:
{markdown_text}
"""

#    stage2_prompt = f"""You are an invoice data structuring engine.

#Given invoice OCR in Markdown, convert it into structured JSON containing ALL invoice fields you can find.
#Requirements:
#1) Preserve information structure (sections/subsections/tables hierarchy).
#2) Keep original field names where possible.
#4) Include all other discovered fields under meaningful section objects.
#5) Do not hallucinate values. Use null when a field is missing.
#6) Return ONLY valid JSON.
#7) Use snake_case keys.
#
#OCR Markdown:
#{markdown_text}
#"""

    structuring_model = choose_structuring_model(available_models)
    stage2_payload = {
        "model": structuring_model,
        "prompt": stage2_prompt,
        "stream": True,
        "temperature": 0.1,
    }

    structured_text = stream_ollama_call(endpoints, stage2_payload, stage_name="STAGE_2_LLAMA_STRUCT")
    if not structured_text:
        print("[STAGE_2_LLAMA_STRUCT] Empty structured output")
        sys.exit(1)

    json_candidate = extract_json_block(structured_text)
    print("PARSED_RESPONSE_FIELD_START")
    try:
        parsed_json = json.loads(json_candidate)
        print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print(structured_text)
    print("PARSED_RESPONSE_FIELD_END")


if __name__ == "__main__":
    main()