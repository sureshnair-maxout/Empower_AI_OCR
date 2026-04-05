"""Llama 3.2 Vision Provider implementation."""

import base64
import html
import json
import logging
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import aiohttp
from PIL import Image, ImageOps

from app.core.config import settings
from app.llm.base import LLMProvider, LLMProviderFactory, OCRField, OCRRequest, OCRResponse

logger = logging.getLogger(__name__)


class LlamaVisionProvider(LLMProvider):
    """Llama 3.2 Vision provider for OCR processing."""

    OUTPUT_SCHEMA_FILE_MAP = {
        "INVOICE": "invoice.json",
        "AADHAAR_CARD": "aadhaar_card.json",
        "PAN_CARD": "pan_card.json",
        "CHEQUE": "cheque.json",
    }

    def __init__(
        self,
        base_url: str = settings.ollama_base_url,
        model_name: str = settings.llama_model_name,
        timeout: int = settings.llm_timeout_seconds,
        max_retries: int = settings.llm_max_retries,
        deployment_mode: str = settings.llm_deployment_mode,
        vm_base_url: str = settings.llm_vm_base_url,
        vm_api_key: str = settings.llm_vm_api_key,
        vm_api_key_header: str = settings.llm_vm_api_key_header,
        vm_enable_thinking: bool = settings.llm_vm_enable_thinking,
        vm_enable_thinking_budget: bool = settings.llm_vm_enable_thinking_budget,
        vm_thinking_budget: int = settings.llm_vm_thinking_budget,
    ):
        """Initialize Llama Vision provider.

        Args:
            base_url: Base URL for Ollama API.
            model_name: Name of the Llama Vision model.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries.
        """
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.timeout = timeout
        self.max_retries = max_retries
        self.deployment_mode = deployment_mode.lower()
        self.vm_base_url = vm_base_url.rstrip("/")
        self.vm_api_key = vm_api_key
        self.vm_api_key_header = vm_api_key_header.lower()
        self.vm_enable_thinking = vm_enable_thinking
        self.vm_enable_thinking_budget = vm_enable_thinking_budget
        self.vm_thinking_budget = vm_thinking_budget

    async def process_ocr(self, request: OCRRequest) -> OCRResponse:
        """Process document using Llama 3.2 Vision model.

        Uses structured prompt engineering optimized for Llama's instruction following.

        Args:
            request: OCR request with document path and metadata.

        Returns:
            OCR response with extracted fields.

        Raises:
            Exception: If OCR processing fails.
        """
        selected_model = request.model_override or self.model_name
        runtime_deployment_mode = (request.deployment_mode_override or self.deployment_mode).lower()

        if runtime_deployment_mode == "vm":
            return await self._process_ocr_vm(request, selected_model)

        doc_path = Path(request.document_path)

        # ===== STAGE 0: IMAGE PREPROCESSING =====
        image_data = await self._preprocess_image(doc_path)
        b64_image = base64.b64encode(image_data).decode("ascii")
        logger.info(f"Encoded image: {len(b64_image)} chars for model {selected_model}")

        # ===== STAGE 1: LLAMA VISION INFERENCE =====
        prompt = self._build_extraction_prompt(request.document_type)
        logger.info(f"Calling Llama Vision with structured extraction prompt...")

        url = f"{self.base_url}/api/generate"
        payload = {
            "model": selected_model,
            "prompt": prompt,
            "images": [b64_image],
            "stream": False,
            "temperature": 0.1,
            "top_p": 0.9,
        }

        last_exc = None
        for attempt in range(max(1, self.max_retries)):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url, json=payload, timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as resp:
                        if resp.status != 200:
                            error_text = await resp.text()
                            raise RuntimeError(f"Llama API failed: {resp.status} - {error_text}")

                        data = await resp.json()
                        response_text = data.get("response", "")
                        logger.info(f"Llama response length: {len(response_text)} chars")
                        print("=" * 80)
                        print("LLAMA RAW RESPONSE:")
                        print(response_text)
                        print("=" * 80)

                        # ===== STAGE 2: PARSE STRUCTURED OUTPUT =====
                        extracted_fields = self._parse_llama_response(response_text)

                        logger.info(
                            "Extracted - invoice_number='%s' invoice_date='%s' total_amount='%s'",
                            extracted_fields.get("invoice_number", "NOT_FOUND"),
                            extracted_fields.get("invoice_date", "NOT_FOUND"),
                            extracted_fields.get("total_amount", "NOT_FOUND"),
                        )

                        # ===== STAGE 3: RETURN STRUCTURED RESPONSE =====
                        fields: dict[str, OCRField] = {}
                        for k, v in extracted_fields.items():
                            fields[k] = OCRField(
                                value=str(v),
                                confidence=1.0,
                                data_type="string",
                                required=False,
                                raw_text=str(v),
                            )

                        return OCRResponse(
                            request_id=str(uuid.uuid4()),
                            document_type=request.document_type,
                            status="success",
                            fields=fields,
                            warnings=[],
                            raw_response={
                                "response_preview": response_text[:500],
                                "model": selected_model,
                            },
                        )

            except Exception as e:
                last_exc = e
                logger.error(f"Attempt {attempt + 1} failed: {e}")

        raise RuntimeError(f"Llama Vision processing failed after retries: {last_exc}")

    def _read_image_as_data_url(self, doc_path: Path) -> str:
        """Read image file and return as data URL preserving original format and quality.

        Mirrors debug_ovis_vm.py exactly — no resizing, no grayscale, no re-encoding.
        For PDFs, renders page 1 as JPEG at 200 DPI without further processing.
        """
        ext = doc_path.suffix.lower()
        if ext == ".pdf":
            try:
                import pdf2image
                images = pdf2image.convert_from_path(str(doc_path), first_page=1, last_page=1, dpi=200)
                if not images:
                    raise RuntimeError("Failed to convert PDF to images")
                import io
                buf = io.BytesIO()
                images[0].save(buf, format="JPEG", quality=95)
                raw = buf.getvalue()
                mime = "image/jpeg"
            except ImportError:
                raise
        else:
            mime_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp",
                ".bmp": "image/bmp",
                ".gif": "image/gif",
            }
            mime = mime_map.get(ext, "image/png")
            raw = doc_path.read_bytes()

        b64 = base64.b64encode(raw).decode("ascii")
        return f"data:{mime};base64,{b64}"

    @staticmethod
    def _is_non_retryable_vm_error(status: int, error_text: str) -> bool:
        """Return True when VM response indicates a deterministic failure.

        These errors are not expected to recover with retries and should fail fast.
        """
        if 400 <= status < 500 and status != 429:
            return True

        lowered = (error_text or "").lower()
        deterministic_markers = [
            "triton",
            "cuda_utils",
            "returned non-zero exit status",
            "/usr/bin/gcc",
            "-lcuda",
            "undefined symbol",
            "cannot open shared object file",
        ]
        return any(marker in lowered for marker in deterministic_markers)

    @staticmethod
    def _build_vm_error_with_hint(error_text: str) -> str:
        """Attach a concise VM-side remediation hint for known runtime failures."""
        lowered = (error_text or "").lower()
        if "triton" in lowered or "cuda_utils" in lowered or "/usr/bin/gcc" in lowered:
            return (
                "VM OCR API runtime failure (non-retryable): "
                f"{error_text}. "
                "Likely VM-side Triton/CUDA toolchain issue. Verify NVIDIA driver visibility, "
                "libcuda availability, and GCC build dependencies on the VM; then restart "
                "the OVIS API server."
            )
        return error_text

    async def _process_ocr_vm(self, request: OCRRequest, selected_model: str) -> OCRResponse:
        """Process OCR using remote VM OpenAI-compatible endpoint on port 8000."""
        doc_path = Path(request.document_path)
        # Use raw image data (no grayscale/resize) to match debug_ovis_vm.py behaviour
        data_url = self._read_image_as_data_url(doc_path)
        prompt = request.prompt_override or self._build_extraction_prompt(request.document_type)
        vm_base_url = (request.vm_base_url_override or self.vm_base_url).rstrip("/")
        headers = self._build_vm_headers()
        url = f"{vm_base_url}/v1/chat/completions"

        payload = {
            "model": selected_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                }
            ],
            "max_tokens": 2048,
            "temperature": 0.0,
            "enable_thinking": False,
            "enable_thinking_budget": False,
            "thinking_budget": self.vm_thinking_budget,
        }

        last_exc = None
        for attempt in range(max(1, self.max_retries)):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url,
                        json=payload,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                    ) as resp:
                        if resp.status != 200:
                            error_text = await resp.text()
                            failure_text = f"VM OCR API failed: {resp.status} - {error_text}"
                            if self._is_non_retryable_vm_error(resp.status, error_text):
                                raise RuntimeError(self._build_vm_error_with_hint(failure_text))
                            raise RuntimeError(failure_text)

                        data = await resp.json()
                        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        json_candidate = self._extract_json_block(content)
                        erp_payload = None

                        fields: dict[str, OCRField] = {}
                        try:
                            parsed = json.loads(json_candidate)
                            if isinstance(parsed, dict):
                                erp_payload = parsed
                                fields = self._flatten_vm_fields(parsed)
                            else:
                                fields["result"] = OCRField(
                                    value=str(parsed),
                                    confidence=1.0,
                                    data_type="string",
                                    required=False,
                                    raw_text=str(parsed),
                                )
                        except json.JSONDecodeError:
                            fields["result"] = OCRField(
                                value=content.strip(),
                                confidence=1.0,
                                data_type="string",
                                required=False,
                                raw_text=content.strip(),
                            )

                        return OCRResponse(
                            request_id=str(uuid.uuid4()),
                            document_type=request.document_type,
                            status="success",
                            fields=fields,
                            warnings=[],
                            erp_payload=erp_payload,
                            raw_response={
                                "model": selected_model,
                                "vm_base_url": vm_base_url,
                                "response_preview": content[:800],
                                "raw_model_output": content,
                            },
                        )
            except Exception as exc:
                last_exc = exc
                logger.error(f"VM attempt {attempt + 1} failed: {exc}")

                # Do not retry deterministic failures that require VM/runtime intervention.
                if isinstance(exc, RuntimeError) and "non-retryable" in str(exc).lower():
                    raise

        raise RuntimeError(f"VM OCR processing failed after retries: {last_exc}")

    def _build_vm_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.vm_api_key:
            if self.vm_api_key_header == "authorization":
                headers["Authorization"] = f"Bearer {self.vm_api_key}"
            else:
                headers["X-API-Key"] = self.vm_api_key
        return headers

    def _extract_json_block(self, text: str) -> str:
        stripped = (text or "").strip()
        think_end = stripped.rfind("</think>")
        if think_end != -1:
            stripped = stripped[think_end + len("</think>") :].strip()
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start != -1 and end != -1 and end > start:
            return stripped[start : end + 1]
        return stripped

    def _flatten_vm_fields(self, parsed: dict) -> dict[str, OCRField]:
        """Flatten nested VM JSON into OCRField entries with confidence support.

        Expected confidence pattern is sibling keys with suffix `_confidence`.
        Example: vendor_name + vendor_name_confidence.
        """

        flattened: dict[str, OCRField] = {}

        def _to_confidence(value: object) -> float:
            try:
                conf = float(value)
                if conf < 0:
                    return 0.0
                if conf > 1:
                    return 1.0
                return conf
            except Exception:
                return 0.0

        def _walk(node: object, prefix: str) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    if key.endswith("_confidence"):
                        continue

                    next_key = f"{prefix}.{key}" if prefix else key

                    if isinstance(value, (dict, list)):
                        _walk(value, next_key)
                        continue

                    confidence = 0.0
                    conf_key = f"{key}_confidence"
                    if conf_key in node:
                        confidence = _to_confidence(node.get(conf_key))

                    value_str = "" if value is None else str(value)
                    flattened[next_key] = OCRField(
                        value=value_str,
                        confidence=confidence,
                        data_type="string",
                        required=False,
                        raw_text=value_str,
                    )
            elif isinstance(node, list):
                for idx, item in enumerate(node):
                    next_key = f"{prefix}[{idx}]" if prefix else f"[{idx}]"
                    _walk(item, next_key)

        _walk(parsed, "")

        if not flattened:
            flattened["result"] = OCRField(
                value=json.dumps(parsed, ensure_ascii=False),
                confidence=0.0,
                data_type="string",
                required=False,
                raw_text=json.dumps(parsed, ensure_ascii=False),
            )

        return flattened

    async def _preprocess_image(self, doc_path: Path) -> bytes:
        """Preprocess and encode image for Llama Vision.

        Args:
            doc_path: Path to document (PDF or image).

        Returns:
            Preprocessed image data as bytes.
        """
        max_width, max_height = 1024, 1024

        if doc_path.suffix.lower() == ".pdf":
            try:
                import pdf2image

                logger.info(f"Converting PDF to image: {doc_path}")
                images = pdf2image.convert_from_path(str(doc_path), first_page=1, last_page=1, dpi=200)
                if not images:
                    raise RuntimeError("Failed to convert PDF to images")
                image = images[0]
            except ImportError:
                logger.error("pdf2image not installed")
                raise
        else:
            image = Image.open(doc_path)

        # Optimize for vision model
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        image = ImageOps.grayscale(image)
        image = ImageOps.autocontrast(image)

        # Save to bytes
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            image.save(tmp.name, "PNG", optimize=True)
            tmp_path = tmp.name

        try:
            with open(tmp_path, "rb") as f:
                image_data = f.read()
        finally:
            import os

            os.unlink(tmp_path)

        return image_data

    def _build_extraction_prompt(self, document_type: str) -> str:
        """Build structured extraction prompt optimized for Llama 3.2.

        Args:
            document_type: Type of document being processed.

        Returns:
            Structured prompt string.
        """
        normalized_doc_type = document_type.upper()
        output_schema = self._load_output_schema(normalized_doc_type)

        if output_schema is not None:
            schema_json = json.dumps(output_schema, ensure_ascii=False, separators=(",", ":"))

            if normalized_doc_type == "INVOICE":
                return (
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
                    f"{schema_json}\n"
                    "Do not add extra keys. Return ONLY valid JSON."
                )

            if normalized_doc_type == "CHEQUE":
                return (
                    "Find the field values in this CHEQUE document and provide output in the required JSON format. "
                    "Output ONLY valid JSON and no other text.\n"
                    "\n"
                    "Standards to follow:\n"
                    "- Turn off reasoning traces and return final JSON only.\n"
                    "- For each extracted field include a corresponding confidence field with a value between 0 and 1.\n"
                    "- ALWAYS set cheque_number from the first portion/segment of the MICR field at the bottom of the cheque.\n"
                    "- Use empty string for missing values and 0 for missing confidence.\n"
                    "\n"
                    "Required JSON structure:\n"
                    f"{schema_json}\n"
                    "Do not add extra keys. Return ONLY valid JSON."
                )

            return (
                f"Find the field values in this {normalized_doc_type} document and provide output in the required JSON format. "
                "Output ONLY valid JSON and no other text.\n"
                "\n"
                "Standards to follow:\n"
                "- Turn off reasoning traces and return final JSON only.\n"
                "- For each extracted field include a corresponding confidence field with a value between 0 and 1.\n"
                "- Use empty string for missing values and 0 for missing confidence.\n"
                "\n"
                "Required JSON structure:\n"
                f"{schema_json}\n"
                "Do not add extra keys. Return ONLY valid JSON."
            )

        # Generic document extraction
        return """Extract all visible text and key information from this document image.
Return the information in a structured JSON format."""

    def _load_output_schema(self, document_type: str) -> Optional[dict]:
        """Load per-document output schema from config/output_schemas."""
        schema_file = self.OUTPUT_SCHEMA_FILE_MAP.get(document_type)
        if not schema_file:
            return None

        schema_path = Path(__file__).resolve().parents[3] / "config" / "output_schemas" / schema_file
        if not schema_path.exists():
            logger.warning("Output schema file not found for %s at %s", document_type, schema_path)
            return None

        try:
            with schema_path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    return loaded
        except Exception as exc:
            logger.warning("Failed to load output schema for %s: %s", document_type, exc)

        return None

    def _parse_llama_response(self, response_text: str) -> dict:
        """Parse Llama's response and extract fields.

        Args:
            response_text: Raw response from Llama model.

        Returns:
            Dictionary with extracted fields.
        """
        import json

        extracted = {
            "invoice_number": "NOT_FOUND",
            "invoice_date": "NOT_FOUND",
            "total_amount": "NOT_FOUND",
        }

        if not response_text:
            return extracted

        # Strategy 1: Try to parse as JSON directly
        try:
            parsed = json.loads(response_text.strip())
            if isinstance(parsed, dict):
                logger.info("Successfully parsed Llama response as JSON")
                # Map fields with validation
                if "invoice_number" in parsed:
                    inv_num = str(parsed["invoice_number"]).strip()
                    if inv_num and not self._looks_like_hash(inv_num):
                        extracted["invoice_number"] = inv_num

                if "invoice_date" in parsed:
                    date_val = str(parsed["invoice_date"]).strip()
                    if date_val and date_val.upper() != "NOT_FOUND":
                        # Validate and normalize date
                        normalized = self._parse_date_to_iso(date_val)
                        extracted["invoice_date"] = normalized

                if "total_amount" in parsed:
                    amount_val = str(parsed["total_amount"]).strip()
                    if amount_val and amount_val.upper() != "NOT_FOUND":
                        # Clean amount
                        cleaned = re.sub(r"[^\d\.]", "", amount_val)
                        if cleaned:
                            extracted["total_amount"] = cleaned

                return extracted
        except json.JSONDecodeError:
            logger.warning("Response is not valid JSON, trying pattern extraction")

        # Strategy 2: Extract JSON from markdown code blocks
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response_text, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group(1))
                if isinstance(parsed, dict):
                    logger.info("Extracted JSON from markdown code block")
                    return self._parse_llama_response(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Strategy 3: Pattern matching for key-value pairs
        logger.info("Falling back to pattern-based extraction")

        # Invoice number patterns
        inv_patterns = [
            r'"invoice_number"\s*:\s*"([^"]+)"',
            r'invoice_number[:\s]+([A-Z0-9\-/]+)',
            r'Invoice\s+No\.?\s*[:\-]?\s*([A-Z0-9\-/]+)',
        ]
        for pattern in inv_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                candidate = match.group(1).strip()
                if candidate and not self._looks_like_hash(candidate):
                    extracted["invoice_number"] = candidate
                    logger.info(f"Found invoice_number via pattern: {candidate}")
                    break

        # Date patterns
        date_patterns = [
            r'"invoice_date"\s*:\s*"([^"]+)"',
            r'invoice_date[:\s]+(\d{4}-\d{2}-\d{2})',
            r'Dated?[:\s]+([0-9A-Za-z\-/]+)',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                candidate = match.group(1).strip()
                normalized = self._parse_date_to_iso(candidate)
                if normalized != "NOT_FOUND":
                    extracted["invoice_date"] = normalized
                    logger.info(f"Found invoice_date via pattern: {normalized}")
                    break

        # Amount patterns
        amount_patterns = [
            r'"total_amount"\s*:\s*"?([0-9,\.]+)"?',
            r'total_amount[:\s]+([0-9,\.]+)',
            r'Total[:\s]+[₹\$]?\s*([0-9,\.]+)',
        ]
        for pattern in amount_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                candidate = match.group(1).strip()
                cleaned = candidate.replace(",", "")
                if cleaned and re.match(r"^\d+(\.\d{2})?$", cleaned):
                    extracted["total_amount"] = cleaned
                    logger.info(f"Found total_amount via pattern: {cleaned}")
                    break

        return extracted

    def _parse_date_to_iso(self, value: str) -> str:
        """Parse date to ISO format (YYYY-MM-DD).

        Args:
            value: Date string in various formats.

        Returns:
            ISO format date or "NOT_FOUND".
        """
        if not value or value.upper() in ("NOT_FOUND", ""):
            return "NOT_FOUND"

        # Already in ISO format
        if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            return value

        candidate = value.strip()

        # Numeric patterns
        numeric_pattern = re.search(r"\b(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})\b", candidate)
        if numeric_pattern:
            raw = numeric_pattern.group(1).replace("/", "-")
            for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y", "%y-%m-%d"):
                try:
                    return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue

        # Text month patterns
        cleaned = re.sub(r"\s+", "-", candidate.replace("/", "-").replace(",", ""))
        cleaned = re.sub(r"-+", "-", cleaned)
        text_match = re.search(r"\b\d{1,2}-[A-Za-z]{3,9}-\d{2,4}\b", cleaned)
        if text_match:
            token = text_match.group(0)
            for fmt in ("%d-%b-%y", "%d-%b-%Y", "%d-%B-%y", "%d-%B-%Y"):
                try:
                    return datetime.strptime(token, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue

        return "NOT_FOUND"

    def _looks_like_hash(self, value: str) -> bool:
        """Check if value looks like a hash or UUID.

        Args:
            value: String to check.

        Returns:
            True if it looks like a hash.
        """
        normalized = value.lower().replace("-", "").replace("_", "")

        # Reject 32+ char hex strings (MD5/SHA)
        if len(normalized) >= 32 and bool(re.fullmatch(r"[0-9a-f]+", normalized)):
            return True

        # Reject long hex sequences
        if re.search(r"[0-9a-f]{16,}", normalized):
            return True

        return False

    async def health_check(self) -> bool:
        """Check Llama Vision API health.

        Returns:
            True if accessible, False otherwise.
        """
        try:
            if self.deployment_mode == "vm":
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.vm_base_url}/health",
                        headers=self._build_vm_headers(),
                        timeout=aiohttp.ClientTimeout(total=5),
                    ) as response:
                        return response.status == 200

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Llama health check failed: {e}")
            return False

    async def get_model_info(self) -> dict:
        """Get Llama model information.

        Returns:
            Dictionary with model metadata.
        """
        try:
            if self.deployment_mode == "vm":
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.vm_base_url}/v1/models",
                        headers=self._build_vm_headers(),
                        timeout=aiohttp.ClientTimeout(total=10),
                    ) as response:
                        if response.status == 200:
                            return await response.json()
                        return {
                            "name": self.model_name,
                            "provider": "llama-vm",
                            "status": f"http_{response.status}",
                        }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/show",
                    params={"name": self.model_name},
                ) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            logger.error(f"Failed to get Llama model info: {e}")

        return {"name": self.model_name, "status": "unknown"}


# Register Llama Vision provider
LLMProviderFactory.register("llama", LlamaVisionProvider)
