"""Sample tests for OCR service."""

import pytest
from app.services.ocr_service import OCRService


@pytest.mark.unit
class TestOCRService:
    """Tests for OCR service."""

    @pytest.fixture
    def ocr_service(self):
        """Create OCR service instance."""
        return OCRService()

    @pytest.mark.asyncio
    async def test_process_document(self, ocr_service):
        """Test document processing."""
        # TODO: Implement actual test
        assert ocr_service is not None

    @pytest.mark.asyncio
    async def test_validate_document_type(self, ocr_service):
        """Test document type validation."""
        # TODO: Implement actual test
        result = await ocr_service.validate_document_type("INVOICE", "org-1")
        assert result is not None
