"""Application constants and enumerations."""

from enum import Enum


class DeploymentMode(str, Enum):
    """Deployment mode options."""

    TENANT = "tenant"
    OWNER = "owner"


class DocumentType(str, Enum):
    """Supported document types."""

    INVOICE = "INVOICE"
    CHEQUE = "CHEQUE"
    PAN_CARD = "PAN_CARD"
    AADHAAR_CARD = "AADHAAR_CARD"


class ConfidenceLevel(str, Enum):
    """Confidence level classifications."""

    HIGH = "HIGH"  # >= 0.9
    MEDIUM = "MEDIUM"  # 0.7 - 0.89
    LOW = "LOW"  # 0.5 - 0.69
    VERY_LOW = "VERY_LOW"  # < 0.5


class FieldDataType(str, Enum):
    """Field data type definitions."""

    STRING = "string"
    INTEGER = "integer"
    DECIMAL = "decimal"
    DATE = "date"
    BOOLEAN = "boolean"
    ARRAY = "array"


class ErrorCode(str, Enum):
    """Application error codes."""

    # Authentication errors
    INVALID_API_KEY = "INVALID_API_KEY"
    EXPIRED_TOKEN = "EXPIRED_TOKEN"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"

    # Document errors
    DOCUMENT_TYPE_MISMATCH = "DOCUMENT_TYPE_MISMATCH"
    UNSUPPORTED_DOCUMENT_TYPE = "UNSUPPORTED_DOCUMENT_TYPE"
    INVALID_DOCUMENT_FORMAT = "INVALID_DOCUMENT_FORMAT"
    DOCUMENT_SIZE_EXCEEDED = "DOCUMENT_SIZE_EXCEEDED"
    CORRUPT_DOCUMENT = "CORRUPT_DOCUMENT"

    # OCR errors
    OCR_PROCESSING_ERROR = "OCR_PROCESSING_ERROR"
    LLM_INFERENCE_ERROR = "LLM_INFERENCE_ERROR"
    MODEL_NOT_AVAILABLE = "MODEL_NOT_AVAILABLE"
    OCR_TIMEOUT = "OCR_TIMEOUT"

    # Validation errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DATA_TYPE_MISMATCH = "DATA_TYPE_MISMATCH"

    # Tenancy errors
    TENANT_NOT_FOUND = "TENANT_NOT_FOUND"
    TENANT_DISABLED = "TENANT_DISABLED"
    TENANT_QUOTA_EXCEEDED = "TENANT_QUOTA_EXCEEDED"

    # Compliance errors
    PII_DETECTED = "PII_DETECTED"
    DATA_LOCALIZATION_VIOLATION = "DATA_LOCALIZATION_VIOLATION"

    # System errors
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    NOT_FOUND = "NOT_FOUND"


class HTTPStatus(int, Enum):
    """HTTP status code mappings for error codes."""

    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    RATE_LIMITED = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


# Map error codes to HTTP status codes
ERROR_CODE_TO_HTTP_STATUS = {
    ErrorCode.INVALID_API_KEY: HTTPStatus.UNAUTHORIZED,
    ErrorCode.EXPIRED_TOKEN: HTTPStatus.UNAUTHORIZED,
    ErrorCode.INSUFFICIENT_PERMISSIONS: HTTPStatus.FORBIDDEN,
    ErrorCode.DOCUMENT_TYPE_MISMATCH: HTTPStatus.UNPROCESSABLE_ENTITY,
    ErrorCode.UNSUPPORTED_DOCUMENT_TYPE: HTTPStatus.BAD_REQUEST,
    ErrorCode.INVALID_DOCUMENT_FORMAT: HTTPStatus.BAD_REQUEST,
    ErrorCode.DOCUMENT_SIZE_EXCEEDED: HTTPStatus.BAD_REQUEST,
    ErrorCode.CORRUPT_DOCUMENT: HTTPStatus.UNPROCESSABLE_ENTITY,
    ErrorCode.OCR_PROCESSING_ERROR: HTTPStatus.INTERNAL_SERVER_ERROR,
    ErrorCode.LLM_INFERENCE_ERROR: HTTPStatus.INTERNAL_SERVER_ERROR,
    ErrorCode.MODEL_NOT_AVAILABLE: HTTPStatus.SERVICE_UNAVAILABLE,
    ErrorCode.OCR_TIMEOUT: HTTPStatus.INTERNAL_SERVER_ERROR,
    ErrorCode.VALIDATION_ERROR: HTTPStatus.UNPROCESSABLE_ENTITY,
    ErrorCode.DATA_TYPE_MISMATCH: HTTPStatus.UNPROCESSABLE_ENTITY,
    ErrorCode.TENANT_NOT_FOUND: HTTPStatus.NOT_FOUND,
    ErrorCode.TENANT_DISABLED: HTTPStatus.FORBIDDEN,
    ErrorCode.TENANT_QUOTA_EXCEEDED: HTTPStatus.RATE_LIMITED,
    ErrorCode.PII_DETECTED: HTTPStatus.UNPROCESSABLE_ENTITY,
    ErrorCode.DATA_LOCALIZATION_VIOLATION: HTTPStatus.FORBIDDEN,
    ErrorCode.INTERNAL_SERVER_ERROR: HTTPStatus.INTERNAL_SERVER_ERROR,
    ErrorCode.SERVICE_UNAVAILABLE: HTTPStatus.SERVICE_UNAVAILABLE,
    ErrorCode.NOT_FOUND: HTTPStatus.NOT_FOUND,
}

# Regex patterns for PII detection
PII_PATTERNS = {
    "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",  # 12-digit Aadhaar
    "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",  # PAN format
    "phone": r"\b(?:\+91|0)\d{10}\b",  # Indian phone numbers
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
}
