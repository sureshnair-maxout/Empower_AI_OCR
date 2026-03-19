"""Ollama LLM Provider implementation."""

import html
import logging
import re
from datetime import datetime
from typing import Optional

import aiohttp
from fuzzywuzzy import fuzz
from PIL import Image

from app.core.config import settings
from app.llm.base import LLMProvider, LLMProviderFactory, OCRRequest, OCRResponse

logger = logging.getLogger(__name__)


class OllamaProvider(LLMProvider):
    """Ollama LLM provider for OCR processing."""

    def __init__(
        self,
        base_url: str = settings.ollama_base_url,
        model_name: str = settings.ocr_model_name,
        timeout: int = settings.llm_timeout_seconds,
        max_retries: int = settings.llm_max_retries,
    ):
        """Initialize Ollama provider.

        Args:
            base_url: Base URL for Ollama API.
            model_name: Name of the OCR model.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries.
        """
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.timeout = timeout
        self.max_retries = max_retries

    async def process_ocr(self, request: OCRRequest) -> OCRResponse:
        """Process document using Ollama with glm-ocr model (dual-prompt strategy).

        Stage 1: Post-processing extraction from raw GLM-OCR output
        - Call "Text Recognition" for full document text
        - Call "Table Recognition" for structured tables
        - Extract fields using fuzzy matching + regex patterns
        - Return structured JSON

        Args:
            request: OCR request with document path and metadata.

        Returns:
            OCR response with extracted fields.

        Raises:
            Exception: If OCR processing fails.
        """
        import uuid
        import base64
        from pathlib import Path
        from PIL import ImageOps
        from app.llm.base import OCRField

        max_width, max_height = 1024, 1024
        doc_path = Path(request.document_path)

        # ===== STAGE 0: IMAGE PREPROCESSING =====
        if doc_path.suffix.lower() == ".pdf":
            try:
                import pdf2image
                logger.info(f"Converting PDF to images: {doc_path}")
                images = pdf2image.convert_from_path(str(doc_path), first_page=1, last_page=1, dpi=200)
                if not images:
                    raise RuntimeError("Failed to convert PDF to images")
                image = images[0]
                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                image = ImageOps.grayscale(image)
                image = ImageOps.autocontrast(image)
                logger.info(f"Resized image to {image.size}")

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
            except ImportError:
                logger.error("pdf2image not installed, falling back to binary")
                with open(doc_path, "rb") as f:
                    image_data = f.read()[:50000]
        else:
            try:
                image = Image.open(doc_path)
                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                image = ImageOps.grayscale(image)
                image = ImageOps.autocontrast(image)

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
            except Exception as img_err:
                logger.warning(f"Failed to resize image: {img_err}, using raw")
                with open(doc_path, "rb") as f:
                    image_data = f.read()

        b64_image = base64.b64encode(image_data).decode("ascii")
        logger.info(f"Encoded image: {len(b64_image)} chars")

        # ===== STAGE 1: DUAL-PROMPT OLLAMA CALLS =====
        url = f"{self.base_url}/api/generate"
        full_text = ""
        table_html = ""

        last_exc = None
        for attempt in range(max(1, self.max_retries)):
            try:
                # Call 1: Text Recognition - get full document text with all fields
                logger.info("Calling Ollama with 'Text Recognition' prompt...")
                payload_text = {
                    "model": self.model_name,
                    "prompt": "Text Recognition",
                    "images": [b64_image],
                    "stream": False,
                    "temperature": 0.1,
                }

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url, json=payload_text, timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as resp:
                        if resp.status != 200:
                            raise RuntimeError(f"Text Recognition failed: {resp.status}")
                        data = await resp.json()
                        full_text = data.get("response", "")
                        logger.info(f"Text Recognition response length: {len(full_text)} chars")

                # Call 2: Table Recognition - get structured HTML table for totals
                logger.info("Calling Ollama with 'Table Recognition' prompt...")
                payload_table = {
                    "model": self.model_name,
                    "prompt": "Table Recognition",
                    "images": [b64_image],
                    "stream": False,
                    "temperature": 0.1,
                }

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url, json=payload_table, timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as resp:
                        if resp.status != 200:
                            logger.warning(f"Table Recognition failed: {resp.status}, continuing without table")
                            table_html = ""
                        else:
                            data = await resp.json()
                            table_html = data.get("response", "")
                            logger.info(f"Table Recognition response length: {len(table_html)} chars")

                # ===== STAGE 2: FIELD EXTRACTION FROM RAW DATA =====
                logger.info("Starting field extraction from raw OCR data...")

                extracted_fields = {
                    "invoice_number": self._extract_invoice_number(full_text),
                    "invoice_date": self._extract_invoice_date(full_text),
                    "total_amount": self._extract_total_amount(full_text, table_html),
                }

                logger.info(
                    "Extracted fields - invoice_number='%s' invoice_date='%s' total_amount='%s'",
                    extracted_fields["invoice_number"],
                    extracted_fields["invoice_date"],
                    extracted_fields["total_amount"],
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
                        "full_text_preview": full_text[:500],
                        "table_html_preview": table_html[:500],
                    },
                )

            except Exception as e:
                last_exc = e
                logger.error(f"Attempt {attempt + 1} failed: {e}")

        raise RuntimeError(f"Ollama processing failed after retries: {last_exc}")

    def _extract_invoice_number(self, text: str) -> str:
        """Extract invoice number using fuzzy label matching.

        Searches for labels like "Invoice No.", "Invoice Number", "Bill No." etc.
        and extracts the value that follows.

        Args:
            text: Full OCR document text.

        Returns:
            Invoice number or "NOT_FOUND".
        """
        if not text:
            return "NOT_FOUND"

        # Define label aliases with fuzzy matching
        label_patterns = [
            ("Invoice No.", r"Invoice\s+No\.?\s*[:\-]?\s*([A-Z0-9\-/]+)"),
            ("Invoice Number", r"Invoice\s+Number\s*[:\-]?\s*([A-Z0-9\-/]+)"),
            ("Bill No.", r"Bill\s+No\.?\s*[:\-]?\s*([A-Z0-9\-/]+)"),
            ("Reference No.", r"Reference\s+No\.?\s*[:\-]?\s*([A-Z0-9\-/]+)"),
        ]

        for label, pattern in label_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                candidate = match.group(1).strip()
                if candidate and not self._looks_like_hash(candidate) and len(candidate) < 50:
                    logger.info(f"Found invoice_number via '{label}' pattern: {candidate}")
                    return candidate

        # Fallback: Look for numeric patterns that look like invoice numbers
        # Typically: digits-digits/digits or similar
        invoice_patterns = [
            r"\b\d{2}[-/]\d{2}/\d{4,}\b",  # 25-26/0077
            r"\b[A-Z]?\d{6,8}\b",  # Simple number pattern
        ]

        for pattern in invoice_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                candidate = match.group(0).strip()
                if not self._looks_like_hash(candidate):
                    logger.info(f"Found invoice_number via fallback pattern: {candidate}")
                    return candidate

        logger.warning("Invoice number not found")
        return "NOT_FOUND"

    def _extract_invoice_date(self, text: str) -> str:
        """Extract invoice date using fuzzy matching and parsing.

        Searches for labels like "Dated", "Date", "Invoice Date" and parses the date.

        Args:
            text: Full OCR document text.

        Returns:
            ISO format date (YYYY-MM-DD) or "NOT_FOUND".
        """
        if not text:
            return "NOT_FOUND"

        # Define label patterns to find dates
        label_patterns = [
            ("Dated", r"Dated\s*[:\-]?\s*([0-9A-Za-z\-/,\s]+?)(?:\n|$)"),
            ("Date", r"(?:Invoice\s+)?Date\s*[:\-]?\s*([0-9A-Za-z\-/,\s]+?)(?:\n|$)"),
            ("Issue Date", r"Issue\s+Date\s*[:\-]?\s*([0-9A-Za-z\-/,\s]+?)(?:\n|$)"),
        ]

        for label, pattern in label_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                candidate = match.group(1).strip()
                if candidate:
                    parsed = self._parse_date_to_iso(candidate)
                    if parsed != "NOT_FOUND":
                        logger.info(f"Found invoice_date via '{label}' pattern: {parsed}")
                        return parsed

        # Fallback: Search for date patterns anywhere in text
        date_patterns = [
            r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b",  # 4-Apr-25 or 04/01/2025
            r"\b(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4})\b",  # 4 Apr 2025
        ]

        for pattern in date_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                candidate = match.group(1).strip()
                parsed = self._parse_date_to_iso(candidate)
                if parsed != "NOT_FOUND":
                    logger.info(f"Found invoice_date via fallback pattern: {parsed}")
                    return parsed

        logger.warning("Invoice date not found")
        return "NOT_FOUND"

    def _extract_total_amount(self, text: str, table_html: str) -> str:
        """Extract total amount from text or HTML table.

        Searches for labels like "Total", "Grand Total" and extracts the amount.
        If table HTML is available, parses it for the final total row.

        Args:
            text: Full OCR document text.
            table_html: HTML table from Table Recognition.

        Returns:
            Total amount as string (e.g., "98537.00") or "NOT_FOUND".
        """
        # Priority 1: Extract from HTML table if available
        if table_html:
            total_from_table = self._extract_from_html_table(table_html)
            if total_from_table != "NOT_FOUND":
                logger.info(f"Found total_amount from HTML table: {total_from_table}")
                return total_from_table

        # Priority 2: Extract from text using label patterns
        if text:
            label_patterns = [
                ("Total", r"Total\s*[:\-]?\s*[₹\$]?\s*([0-9,\.]+)"),
                ("Grand Total", r"Grand\s+Total\s*[:\-]?\s*[₹\$]?\s*([0-9,\.]+)"),
                ("Net Payable", r"Net\s+Payable\s*[:\-]?\s*[₹\$]?\s*([0-9,\.]+)"),
            ]

            for label, pattern in label_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    candidate = match.group(1).strip()
                    normalized = candidate.replace(",", "").replace("₹", "").strip()
                    if normalized and re.match(r"^\d+(\.\d{2})?$", normalized):
                        logger.info(f"Found total_amount via '{label}' pattern: {normalized}")
                        return normalized

            # Fallback: Find largest currency amount
            amount_pattern = r"[₹\$]?\s*([0-9]{1,3}(?:,\d{3})*(?:\.\d{2})?)"
            matches = re.finditer(amount_pattern, text)
            amounts = []
            for match in matches:
                try:
                    amount_str = match.group(1).replace(",", "")
                    amount_num = float(amount_str)
                    amounts.append((amount_num, amount_str))
                except (ValueError, AttributeError):
                    pass

            if amounts:
                largest = max(amounts, key=lambda x: x[0])
                result = largest[1]
                logger.info(f"Found total_amount via largest amount fallback: {result}")
                return result

        logger.warning("Total amount not found")
        return "NOT_FOUND"

    def _extract_from_html_table(self, html_text: str) -> str:
        """Extract total amount from HTML table.

        Looks for the last row with "Total" label and extracts the amount.

        Args:
            html_text: HTML table string.

        Returns:
            Total amount or "NOT_FOUND".
        """
        if not html_text:
            return "NOT_FOUND"

        # Unescape HTML entities
        html_text = html.unescape(html_text)

        # Find rows (simplified - look for <tr> ... </tr>)
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html_text, re.DOTALL | re.IGNORECASE)
        
        if not rows:
            return "NOT_FOUND"

        # Process rows in reverse to find Total row
        for row in reversed(rows):
            # Check if this row contains "Total"
            if "total" in row.lower():
                # Extract all cell values
                cells = re.findall(r"<t[dh][^>]*>([^<]*)</t[dh]>", row, re.IGNORECASE)
                # Look for amounts in cells
                for cell in cells:
                    cell_text = cell.strip()
                    # Try to parse as amount
                    amount_match = re.search(r"([0-9]{1,3}(?:,\d{3})*(?:\.\d{2})?)", cell_text)
                    if amount_match:
                        amount = amount_match.group(1).replace(",", "")
                        if float(amount) > 0:
                            return amount

        return "NOT_FOUND"

    def _parse_date_to_iso(self, value: str) -> str:
        """Parse date in various formats to ISO (YYYY-MM-DD).

        Args:
            value: Date string in various formats.

        Returns:
            ISO format date or "NOT_FOUND".
        """
        if not value or value.upper() in ("NOT_FOUND", "YYYY-MM-DD", ""):
            return "NOT_FOUND"

        candidate = value.strip()

        # Numeric patterns: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
        numeric_pattern = re.search(r"\b(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})\b", candidate)
        if numeric_pattern:
            raw = numeric_pattern.group(1).replace("/", "-")
            for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d-%m-%y", "%y-%m-%d"):
                try:
                    return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue

        # Text month patterns: 4-Apr-25, 04 April 2025, etc.
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
        """Check if value looks like a hash, UUID, or long hex string.

        Args:
            value: String to check.

        Returns:
            True if it looks like a hash (should be rejected), False otherwise.
        """
        normalized = value.lower().replace("-", "").replace("_", "")

        # Reject if mostly hex and 32+ chars (likely MD5/SHA hash)
        if len(normalized) >= 32 and bool(re.fullmatch(r"[0-9a-f]+", normalized)):
            return True

        # Reject if contains long continuous hex sequences (16+ chars)
        long_hex_pattern = re.search(r"[0-9a-f]{16,}", normalized)
        return bool(long_hex_pattern)

    async def health_check(self) -> bool:
        """Check Ollama API health.

        Returns:
            True if Ollama is accessible, False otherwise.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False

    async def get_model_info(self) -> dict:
        """Get model information from Ollama.

        Returns:
            Dictionary with model metadata.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/show",
                    params={"name": self.model_name},
                ) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")

        return {
            "name": self.model_name,
            "status": "unknown",
        }


# Register Ollama provider
LLMProviderFactory.register("ollama", OllamaProvider)
