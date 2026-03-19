"""Pydantic schemas for API requests and responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Organization Schemas
class OrganizationBase(BaseModel):
    """Base organization schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    deployment_mode: str = "tenant"
    billing_enabled: bool = True


class OrganizationCreate(OrganizationBase):
    """Create organization schema."""

    pass


class OrganizationResponse(OrganizationBase):
    """Organization response schema."""

    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# API Key Schemas
class APIKeyCreate(BaseModel):
    """Create API key schema."""

    name: str = Field(..., min_length=1, max_length=255)


class APIKeyResponse(BaseModel):
    """API key response schema."""

    id: str
    name: str
    is_active: bool
    last_used: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class APIKeySecret(BaseModel):
    """API key with secret (only shown once)."""

    id: str
    key: str  # The actual API key
    name: str


# Document OCR Schemas
class OCRFieldResponse(BaseModel):
    """OCR extracted field response."""

    value: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    data_type: str
    required: bool
    raw_text: Optional[str] = None


class OCRProcessRequest(BaseModel):
    """OCR processing request."""

    document_type_code: str = Field(..., min_length=1)
    # document_image is passed as multipart form data


class OCRProcessResponse(BaseModel):
    """OCR processing response."""

    request_id: str
    document_type: str
    status: str  # success, partial, failed
    ocr_results: dict[str, OCRFieldResponse]
    confidence_level: str  # HIGH, MEDIUM, LOW, VERY_LOW
    processing_time_ms: int
    warnings: list[str] = []
    errors: list[str] = []
    model_version: Optional[str] = None
    erp_payload: Optional[dict] = None  # Ready-to-send payload
    raw_model_output: Optional[str] = None  # Untruncated raw text from the model

    class Config:
        from_attributes = True


# Billing Schemas
class BillingRecordResponse(BaseModel):
    """Billing record response."""

    id: str
    document_type: str
    rate_per_document: float
    amount: float
    billing_period: str
    status: str
    used_date: datetime

    class Config:
        from_attributes = True


class BillingAggregateResponse(BaseModel):
    """Aggregated billing response."""

    org_id: str
    billing_period: str
    total_documents: int
    total_amount: float
    status: str
    records: list[BillingRecordResponse]


class BillingDashboardResponse(BaseModel):
    """Billing dashboard data."""

    current_period: str
    monthly_total: float
    document_count: int
    breakdown_by_type: dict[str, dict]
    trend_data: list[dict]


# Error Schemas
class ErrorDetail(BaseModel):
    """Error response detail."""

    error_code: str
    message: str
    details: Optional[str] = None
    request_id: Optional[str] = None


class ValidationErrorDetail(BaseModel):
    """Validation error detail."""

    field: str
    error: str
    value: Optional[str] = None


# Health Check
class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str
    app: str
    version: str
    environment: str
    timestamp: datetime
    components: Optional[dict] = None
