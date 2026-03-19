"""LLM Provider abstraction layer."""

from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel


class OCRRequest(BaseModel):
    """OCR request data."""

    document_path: str
    document_type: str
    prompt_override: Optional[str] = None
    model_override: Optional[str] = None
    deployment_mode_override: Optional[str] = None
    vm_base_url_override: Optional[str] = None


class OCRField(BaseModel):
    """OCR extracted field."""

    value: str
    confidence: float
    data_type: str
    required: bool
    raw_text: Optional[str] = None


class OCRResponse(BaseModel):
    """OCR response data."""

    request_id: str
    document_type: str
    status: str  # success, partial, failed
    fields: dict[str, OCRField]
    warnings: list[str] = []
    errors: list[str] = []
    erp_payload: Optional[dict] = None
    raw_response: Optional[dict] = None


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def process_ocr(self, request: OCRRequest) -> OCRResponse:
        """Process document for OCR.

        Args:
            request: OCR request with document path and metadata.

        Returns:
            OCR response with extracted fields and confidence scores.

        Raises:
            Exception: If OCR processing fails.
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the LLM provider is healthy and accessible.

        Returns:
            True if provider is healthy, False otherwise.
        """
        pass

    @abstractmethod
    async def get_model_info(self) -> dict:
        """Get information about the current model.

        Returns:
            Dictionary with model metadata (name, version, etc.).
        """
        pass


class LLMProviderFactory:
    """Factory for creating LLM provider instances."""

    _providers: dict = {}

    @classmethod
    def register(cls, provider_name: str, provider_class: type):
        """Register a provider.

        Args:
            provider_name: Name of the provider (e.g., 'ollama', 'sglang').
            provider_class: Provider class implementing LLMProvider.
        """
        cls._providers[provider_name.lower()] = provider_class

    @classmethod
    def create(cls, provider_name: str, **config) -> LLMProvider:
        """Create a provider instance.

        Args:
            provider_name: Name of the provider.
            **config: Configuration arguments for the provider.

        Returns:
            LLMProvider instance.

        Raises:
            ValueError: If provider is not registered.
        """
        provider_class = cls._providers.get(provider_name.lower())
        if not provider_class:
            raise ValueError(f"Unknown LLM provider: {provider_name}")
        return provider_class(**config)


class ProviderNotImplementedError(Exception):
    """Exception for unimplemented provider."""

    pass
