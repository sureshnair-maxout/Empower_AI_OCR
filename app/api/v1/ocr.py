"""OCR endpoints."""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pathlib import Path
import uuid
import shutil

from app.auth.api_key import verify_api_key
from app.schemas.schemas import OCRProcessResponse, ErrorDetail
from app.services.ocr_service import OCRService
from app.tenancy.context import set_org_context, get_current_org

router = APIRouter()
ocr_service = OCRService()


@router.post("/ocr/process", response_model=OCRProcessResponse)
async def process_document(
    file: UploadFile = File(...),
    document_type_code: str = Form(...),
    provider_name: str | None = Form(None),
    deployment_mode: str | None = Form(None),
    vm_base_url: str | None = Form(None),
    model_name: str | None = Form(None),
    prompt_override: str | None = Form(None),
    auth: dict = Depends(verify_api_key),
):
    """Process a document for OCR.

    Args:
        file: Document file (JPG, PNG, PDF).
        document_type_code: Type of document (INVOICE, CHEQUE, PAN_CARD, AADHAAR_CARD).
        auth: Authentication data from API key.

    Returns:
        OCR processing result with extracted fields.

    Raises:
        HTTPException: If document is invalid or processing fails.
    """
    org_id = auth.get("org_id")
    set_org_context(org_id)

    try:
        # Validate file format & size could be added here
        # Save uploaded file to configured storage path
        storage_dir = Path("./storage/documents")
        storage_dir.mkdir(parents=True, exist_ok=True)
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        dest_path = storage_dir / filename
        with dest_path.open("wb") as out_file:
            shutil.copyfileobj(file.file, out_file)

        current_org = await get_current_org()
        result = await ocr_service.process_document(
            file_path=str(dest_path),
            document_type=document_type_code,
            org_id=current_org,
            provider_override=provider_name,
            deployment_mode_override=deployment_mode,
            vm_base_url_override=vm_base_url,
            model_override=model_name,
            prompt_override=prompt_override,
        )

        # Map provider response into API response
        raw_resp = result.get("raw_response") or {}
        return OCRProcessResponse(
            request_id=result.get("request_id"),
            document_type=result.get("document_type"),
            status=result.get("status"),
            ocr_results=result.get("fields", {}),
            confidence_level=result.get("confidence", "UNKNOWN"),
            processing_time_ms=result.get("processing_time_ms", 0),
            warnings=result.get("warnings", []),
            errors=result.get("errors", []),
            model_version=raw_resp.get("model"),
            erp_payload=result.get("erp_payload"),
            raw_model_output=raw_resp.get("raw_model_output"),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/ocr/health")
async def ocr_health(auth: dict = Depends(verify_api_key)):
    """Check OCR processing health.

    Returns:
        Health status of OCR components.
    """
    try:
        is_healthy = await ocr_service.llm_provider.health_check()
        model_info = await ocr_service.llm_provider.get_model_info()

        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "provider": "ollama",
            "model": model_info,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"OCR service unavailable: {str(e)}",
        )
