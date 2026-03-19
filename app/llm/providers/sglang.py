"""SGLang LLM Provider implementation."""

import logging

from app.llm.base import LLMProvider, LLMProviderFactory, OCRRequest, OCRResponse

logger = logging.getLogger(__name__)


class SGLangProvider(LLMProvider):
    """SGLang LLM provider for OCR processing."""

    def __init__(
        self,
        base_url: str = "http://localhost:30000",
        model_name: str = "glm-ocr",
        timeout: int = 120,
        max_retries: int = 3,
    ):
        """Initialize SGLang provider.

        Args:
            base_url: Base URL for SGLang API.
            model_name: Name of the OCR model.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries.
        """
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.timeout = timeout
        self.max_retries = max_retries

    async def process_ocr(self, request: OCRRequest) -> OCRResponse:
        """Process document using SGLang.

        Args:
            request: OCR request with document path and metadata.

        Returns:
            OCR response with extracted fields.

        Raises:
            Exception: If OCR processing fails.
        """
        # TODO: Implement document loading
        # TODO: Create prompt from template
        # TODO: Call SGLang API
        # TODO: Parse response and extract fields
        # TODO: Calculate confidence scores

        import uuid

        return OCRResponse(
            request_id=str(uuid.uuid4()),
            document_type=request.document_type,
            status="success",
            fields={},
            warnings=["SGLang provider not yet fully implemented"],
        )

    async def health_check(self) -> bool:
        """Check SGLang API health.

        Returns:
            True if SGLang is accessible, False otherwise.
        """
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/health",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    return response.status == 200
        except Exception as e:
            logger.error(f"SGLang health check failed: {e}")
            return False

    async def get_model_info(self) -> dict:
        """Get model information from SGLang.

        Returns:
            Dictionary with model metadata.
        """
        return {
            "name": self.model_name,
            "provider": "sglang",
            "status": "available",
        }


# Register SGLang provider
LLMProviderFactory.register("sglang", SGLangProvider)
