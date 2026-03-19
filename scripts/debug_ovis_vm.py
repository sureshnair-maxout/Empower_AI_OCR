import argparse
import base64
import json
from pathlib import Path
from typing import Optional

import requests


def read_image_as_data_url(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    if ext in {".jpg", ".jpeg"}:
        mime = "image/jpeg"
    elif ext == ".webp":
        mime = "image/webp"
    elif ext == ".bmp":
        mime = "image/bmp"
    elif ext == ".gif":
        mime = "image/gif"
    else:
        mime = "image/png"

    content = file_path.read_bytes()
    b64 = base64.b64encode(content).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def candidate_base_urls(vm_url: str) -> list[str]:
    vm_url = vm_url.strip().rstrip("/")
    candidates = [vm_url]

    if vm_url.startswith("http://") or vm_url.startswith("https://"):
        # Try common service ports if user gave only host URL.
        scheme, rest = vm_url.split("://", 1)
        host = rest.split("/", 1)[0]
        candidates.extend(
            [
                f"{scheme}://{host}:8000",
                f"{scheme}://{host}:11434",
                f"{scheme}://{host}:7860",
                f"{scheme}://{host}",
            ]
        )
    else:
        # Bare hostname/IP
        candidates.extend(
            [
                f"https://{vm_url}",
                f"http://{vm_url}",
                f"https://{vm_url}:8000",
                f"http://{vm_url}:8000",
                f"https://{vm_url}:11434",
                f"http://{vm_url}:11434",
                f"https://{vm_url}:7860",
                f"http://{vm_url}:7860",
            ]
        )

    deduped = []
    seen = set()
    for item in candidates:
        if item not in seen:
            deduped.append(item)
            seen.add(item)
    return deduped


def build_headers(api_key: Optional[str], x_api_key: Optional[str]) -> dict:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    if x_api_key:
        headers["X-API-Key"] = x_api_key
    return headers


def probe_endpoints(
    base_urls: list[str],
    headers: dict,
    timeout: int,
    verify_ssl: bool,
) -> dict:
    checks = [
        ("openai_models", "/v1/models"),
        ("openai_chat", "/v1/chat/completions"),
        ("ollama_tags", "/api/tags"),
        ("ollama_generate", "/api/generate"),
        ("gradio_root", "/"),
        ("gradio_info", "/info"),
        ("gradio_config", "/config"),
    ]

    result = {}
    for base in base_urls:
        result[base] = {}
        for name, path in checks:
            url = f"{base.rstrip('/')}{path}"
            try:
                if name in {"openai_chat", "ollama_generate"}:
                    # lightweight POST shape check
                    payload = {"model": "dummy", "stream": False}
                    response = requests.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=timeout,
                        verify=verify_ssl,
                    )
                else:
                    response = requests.get(
                        url,
                        headers=headers,
                        timeout=timeout,
                        verify=verify_ssl,
                    )
                result[base][name] = {
                    "status": response.status_code,
                    "url": url,
                    "ok": response.status_code < 500,
                    "body_preview": response.text[:300],
                }
            except Exception as exc:
                result[base][name] = {
                    "status": None,
                    "url": url,
                    "ok": False,
                    "error": str(exc),
                }
    return result


def choose_openai_base(probe: dict) -> Optional[str]:
    for base, checks in probe.items():
        models = checks.get("openai_models", {})
        if models.get("status") == 200:
            return base
    return None


def choose_gradio_base(probe: dict) -> Optional[str]:
    for base, checks in probe.items():
        root = checks.get("gradio_root", {})
        config = checks.get("gradio_config", {})
        info = checks.get("gradio_info", {})
        if root.get("status") == 200 or config.get("status") == 200 or info.get("status") == 200:
            return base
    return None


def extract_json_block(text: str) -> str:
    stripped = text.strip()

    think_end = stripped.rfind("</think>")
    if think_end != -1:
        stripped = stripped[think_end + len("</think>") :].strip()

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end != -1 and end > start:
        return stripped[start : end + 1]
    return stripped


def call_openai_vision(
    base_url: str,
    model: str,
    prompt: str,
    image_data_url: str,
    headers: dict,
    timeout: int,
    verify_ssl: bool,
    max_tokens: int,
    temperature: float,
    enable_thinking: bool,
    enable_thinking_budget: bool,
    thinking_budget: int,
) -> requests.Response:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                ],
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "enable_thinking": enable_thinking,
        "enable_thinking_budget": enable_thinking_budget,
        "thinking_budget": thinking_budget,
    }
    url = f"{base_url.rstrip('/')}/v1/chat/completions"
    return requests.post(url, headers=headers, json=payload, timeout=timeout, verify=verify_ssl)


def main() -> None:
    parser = argparse.ArgumentParser(description="Test Ovis model hosted on remote VM")
    parser.add_argument("--vm-url", required=True, help="VM URL/IP/hostname")
    parser.add_argument("--model", default="AIDC-AI/Ovis2.5-9B", help="Remote model ID")
    parser.add_argument("--file", required=True, help="Local image path to send")
    parser.add_argument("--api-key", default=None, help="Bearer token")
    parser.add_argument("--x-api-key", default=None, help="X-API-Key value")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--enable-thinking", action="store_true", help="Enable Ovis thinking mode")
    parser.add_argument("--enable-thinking-budget", action="store_true", help="Enable Ovis thinking budget")
    parser.add_argument("--thinking-budget", type=int, default=512)
    parser.add_argument("--insecure", action="store_true", help="Skip TLS verification")
    parser.add_argument("--output", default="ovis_vm_debug_result.json")
    parser.add_argument(
        "--prompt",
        default=(
            "Find the field values in the document and provide in the JSON format as given below. Output ONLY the JSON format, no other text outputs.\n"
            "\n"
            "Standards to follow:\n"
            "- Turn off reasoning traces and return final JSON only.\n"
            "- For each extracted field include a corresponding confidence field with a value between 0 and 1.\n"
            "- GST Number (GSTIN) must follow format ##AAAAA####A#Z#.\n"
            "- quantity, rate, and amount must be numeric only with no UOM or currency indicators.\n"
            "- Repeat item objects in items for as many invoice line items as are present.\n"
            "- Use empty string for missing values and 0 for missing confidence.\n"
            "\n"
            "Required JSON structure:\n"
            "{"
            "\"vendor_details\":{\"vendor_name\":\"\",\"vendor_name_confidence\":0,\"vendor_address\":\"\",\"vendor_address_confidence\":0,\"vendor_gst_no\":\"\",\"vendor_gst_no_confidence\":0,\"vendor_mobile_no_1\":\"\",\"vendor_mobile_no_1_confidence\":0,\"vendor_mobile_no_2\":\"\",\"vendor_mobile_no_2_confidence\":0,\"email_id\":\"\",\"email_id_confidence\":0,\"agent_broker_name\":\"\",\"agent_broker_name_confidence\":0},"
            "\"invoice_details\":{\"invoice_date\":\"\",\"invoice_date_confidence\":0,\"invoice_no\":\"\",\"invoice_no_confidence\":0,\"invoice_type\":\"\",\"invoice_type_confidence\":0,\"bill_to\":\"\",\"bill_to_confidence\":0,\"po_no\":\"\",\"po_no_confidence\":0,\"eway_bill_no\":\"\",\"eway_bill_no_confidence\":0,\"acknowledge_no\":\"\",\"acknowledge_no_confidence\":0},"
            "\"transport_details\":{\"vehicle_no\":\"\",\"vehicle_no_confidence\":0,\"driver_name\":\"\",\"driver_name_confidence\":0,\"driver_no\":\"\",\"driver_no_confidence\":0},"
            "\"bank_details\":{\"account_holder_name\":\"\",\"account_holder_name_confidence\":0,\"account_number\":\"\",\"account_number_confidence\":0,\"ifsc_code\":\"\",\"ifsc_code_confidence\":0},"
            "\"items\":[{\"item_no\":\"\",\"item_no_confidence\":0,\"item_name\":\"\",\"item_name_confidence\":0,\"hsn_code\":\"\",\"hsn_code_confidence\":0,\"gst_percent\":\"\",\"gst_percent_confidence\":0,\"uom\":\"\",\"uom_confidence\":0,\"quantity\":\"\",\"quantity_confidence\":0,\"rate\":\"\",\"rate_confidence\":0,\"amount\":\"\",\"amount_confidence\":0}]"
            "}\n"
            "Do not add extra keys. Return ONLY valid JSON."
        ),
    )

    args = parser.parse_args()

    local_file = Path(args.file)
    if not local_file.exists():
        raise FileNotFoundError(f"Input file not found: {local_file}")

    headers = build_headers(args.api_key, args.x_api_key)
    bases = candidate_base_urls(args.vm_url)

    print("Probing remote VM endpoints...")
    probe = probe_endpoints(
        base_urls=bases,
        headers=headers,
        timeout=args.timeout,
        verify_ssl=not args.insecure,
    )

    openai_base = choose_openai_base(probe)
    gradio_base = choose_gradio_base(probe)

    output = {
        "vm_url": args.vm_url,
        "candidates": bases,
        "probe": probe,
        "selected_openai_base": openai_base,
        "selected_gradio_base": gradio_base,
    }

    if not openai_base:
        if gradio_base:
            print(
                "No OpenAI-compatible endpoint discovered, but Gradio UI is reachable at "
                f"{gradio_base}. Expose an API server on port 8000 or 11434 for integration."
            )
        else:
            print("No OpenAI-compatible endpoint discovered. Check NSG/firewall/service binding.")
        Path(args.output).write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Saved debug output to {args.output}")
        return

    print(f"Using endpoint: {openai_base}")
    data_url = read_image_as_data_url(local_file)

    response = call_openai_vision(
        base_url=openai_base,
        model=args.model,
        prompt=args.prompt,
        image_data_url=data_url,
        headers=headers,
        timeout=max(args.timeout, 300),
        verify_ssl=not args.insecure,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        enable_thinking=args.enable_thinking,
        enable_thinking_budget=args.enable_thinking_budget,
        thinking_budget=args.thinking_budget,
    )

    output["invoke_status"] = response.status_code
    output["invoke_raw"] = response.text

    print(f"Invoke status: {response.status_code}")
    print("RAW_RESPONSE_START")
    print(response.text)
    print("RAW_RESPONSE_END")

    try:
        parsed = response.json()
        output["invoke_parsed"] = parsed
        content = parsed.get("choices", [{}])[0].get("message", {}).get("content", "")
        output["invoke_content"] = content
        json_candidate = extract_json_block(content)
        output["invoke_json_candidate"] = json_candidate
        try:
            output["invoke_json"] = json.loads(json_candidate)
        except json.JSONDecodeError:
            pass
        print("PARSED_RESPONSE_FIELD_START")
        print(content)
        print("PARSED_RESPONSE_FIELD_END")
    except Exception:
        pass

    Path(args.output).write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved debug output to {args.output}")


if __name__ == "__main__":
    main()
