"""OCR service business logic."""

import logging
import time
import uuid
from typing import Optional

from app.core.config import settings
from app.llm.base import LLMProviderFactory, OCRRequest

logger = logging.getLogger(__name__)


class DocumentTypeError(Exception):
    """Document type validation error."""

    pass


class OCRService:
    """Service for OCR processing."""

    def __init__(self):
        """Initialize OCR service."""
        self.llm_provider = self._create_provider(settings.llm_provider)

    def _create_provider(self, provider_name: str):
        provider_name = provider_name.lower()

        provider_config = {
            "base_url": settings.ollama_base_url,
            "model_name": settings.ocr_model_name,
            "timeout": settings.llm_timeout_seconds,
        }

        if provider_name == "llama":
            provider_config.update(
                {
                    "model_name": settings.llama_model_name,
                    "deployment_mode": settings.llm_deployment_mode,
                    "vm_base_url": settings.llm_vm_base_url,
                    "vm_api_key": settings.llm_vm_api_key,
                    "vm_api_key_header": settings.llm_vm_api_key_header,
                    "vm_enable_thinking": settings.llm_vm_enable_thinking,
                    "vm_enable_thinking_budget": settings.llm_vm_enable_thinking_budget,
                    "vm_thinking_budget": settings.llm_vm_thinking_budget,
                }
            )
        elif provider_name == "ollama":
            provider_config["model_name"] = settings.glm_ocr_model_name

        return LLMProviderFactory.create(provider_name, **provider_config)

    async def process_document(
        self,
        file_path: str,
        document_type: str,
        org_id: str,
        provider_override: Optional[str] = None,
        deployment_mode_override: Optional[str] = None,
        vm_base_url_override: Optional[str] = None,
        model_override: Optional[str] = None,
        prompt_override: Optional[str] = None,
    ) -> dict:
        """Process a document for OCR.

        Args:
            file_path: Path to the document file.
            document_type: Type of document.
            org_id: Organization ID.

        Returns:
            OCR processing result.

        Raises:
            DocumentTypeError: If document type is invalid.
            Exception: If OCR processing fails.
        """
        request_id = str(uuid.uuid4())
        logger.info(
            f"Starting OCR processing for document type {document_type}",
            extra={
                "request_id": request_id,
                "org_id": org_id,
                "document_type": document_type,
            },
        )

        try:
            start_time = time.perf_counter()
            # TODO: Validate document type against schema
            # TODO: Validate document format and size
            # TODO: Load document from storage

            # Create OCR request
            ocr_request = OCRRequest(
                document_path=file_path,
                document_type=document_type,
                deployment_mode_override=deployment_mode_override,
                vm_base_url_override=vm_base_url_override,
                model_override=model_override,
                prompt_override=prompt_override,
            )

            # Process with LLM provider
            llm_provider = self.llm_provider
            if provider_override:
                llm_provider = self._create_provider(provider_override)

            ocr_response = await llm_provider.process_ocr(ocr_request)
            ocr_response.request_id = request_id

            logger.info(
                f"OCR processing completed successfully",
                extra={
                    "request_id": request_id,
                    "org_id": org_id,
                    "status": ocr_response.status,
                },
            )
            payload = ocr_response.model_dump()
            processing_time_ms = int((time.perf_counter() - start_time) * 1000)

            fields = payload.get("fields", {})
            field_confidences: list[float] = []
            if isinstance(fields, dict):
                for field in fields.values():
                    if isinstance(field, dict) and "confidence" in field:
                        try:
                            field_confidences.append(float(field.get("confidence", 0.0)))
                        except Exception:
                            pass

            avg_confidence = sum(field_confidences) / len(field_confidences) if field_confidences else 0.0

            if avg_confidence >= 0.9:
                confidence_level = "HIGH"
            elif avg_confidence >= 0.75:
                confidence_level = "MEDIUM"
            elif avg_confidence >= 0.5:
                confidence_level = "LOW"
            else:
                confidence_level = "VERY_LOW"

            payload["processing_time_ms"] = processing_time_ms
            payload["confidence"] = confidence_level
            return payload

        except Exception as e:
            logger.error(
                f"OCR processing failed: {str(e)}",
                extra={
                    "request_id": request_id,
                    "org_id": org_id,
                },
                exc_info=True,
            )
            raise

    async def validate_document_type(self, document_type: str, org_id: str) -> dict:
        """Validate and get document type schema.

        Args:
            document_type: Document type code.
            org_id: Organization ID.

        Returns:
            Document type schema.

        Raises:
            DocumentTypeError: If document type is not found.
        """
        # TODO: Query database for document type schema
        # For now, return placeholder
        return {
            "code": document_type,
            "name": document_type,
            "schema": {},
        }

    async def detect_document_type(self, file_path: str) -> str:
        """Detect document type from image.

        Args:
            file_path: Path to the document file.

        Returns:
            Detected document type code.
        """
        # TODO: Implement document type detection using initial OCR pass
        return "UNKNOWN"
