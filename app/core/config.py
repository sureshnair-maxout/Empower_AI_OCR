"""Application configuration management."""

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

# Explicitly load .env file before settings are initialized
# This ensures env vars are available even when run as a script
env_file = Path(__file__).parent.parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file, override=False)

# Normalize any comma-separated list values into JSON arrays so pydantic's
# EnvSettingsSource won't choke when it tries to decode as JSON.
for key in (
    "SUPPORTED_FORMATS",
    "CORS_ORIGINS",
    "CORS_ALLOW_METHODS",
    "CORS_ALLOW_HEADERS",
    "PII_FIELDS",
):
    raw = os.getenv(key)
    if raw and not raw.strip().startswith("["):
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        os.environ[key] = json.dumps(parts)



class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Empower AI OCR API"
    app_version: str = "1.0.0"
    app_env: Literal["development", "staging", "production"] = "development"
    api_prefix: str = "/api/v1"
    secret_key: str = "your-secret-key-change-in-production-min-32-chars"
    debug: bool = True

    # Deployment Mode
    deployment_mode: Literal["tenant", "owner"] = "tenant"
    enable_billing: bool = True

    # Database
    # Use asyncpg for SQLAlchemy async engine
    database_url: str = "postgresql+asyncpg://ocr_user:ocr_password@localhost:5432/ocr_db"
    database_pool_size: int = 10
    database_echo: bool = False

    # Authentication & Security
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"
    jwt_subject: str = "access_token"

    # India Compliance
    data_localization_enabled: bool = True
    enforce_pii_handling: bool = True
    pii_fields: list[str] = ["aadhaar_number", "pan_number", "phone_number", "email"]

    # LLM Configuration
    llm_provider: str = "llama"  # Options: "ollama" (GLM-OCR), "llama" (Llama 3.2 Vision)
    ollama_base_url: str = "http://localhost:11434"
    llm_deployment_mode: Literal["local", "vm"] = "local"
    llm_vm_base_url: str = "http://localhost:8000"
    llm_vm_api_key: str = ""
    llm_vm_api_key_header: Literal["x-api-key", "authorization"] = "x-api-key"
    llm_vm_enable_thinking: bool = False
    llm_vm_enable_thinking_budget: bool = False
    llm_vm_thinking_budget: int = 512
    
    # GLM-OCR Model Settings (provider="ollama")
    glm_ocr_model_name: str = "glm-ocr:latest"
    
    # Llama 3.2 Vision Model Settings (provider="llama")
    llama_model_name: str = "llama3.2-vision:11b"
    
    # General LLM Settings
    ocr_model_name: str = "glm-ocr"  # Deprecated - use specific model configs
    ocr_model_version: str = "latest"
    llm_timeout_seconds: int = 180
    llm_max_retries: int = 3

    # Document Configuration
    document_type_config_path: str = "./config/document_types.yaml"
    max_document_size_mb: int = 20
    supported_formats: list[str] = ["jpg", "jpeg", "png", "pdf"]

    @field_validator("database_url", mode="before")
    @classmethod
    def ensure_async_driver(cls, v: Any) -> Any:
        """Make sure the URL uses asyncpg when PostgreSQL is referenced.

        Some dotenv parsers (on Windows) may strip the "+asyncpg" portion from
        the value.  If the incoming string looks like a bare
        "postgresql://" URL we automatically insert "+asyncpg" so the async
        engine will function correctly.
        """
        if isinstance(v, str) and v.startswith("postgresql://") and "+asyncpg" not in v:
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    # Observability
    otel_enabled: bool = True
    otel_exporter_type: str = "otlp"
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    jaeger_enabled: bool = False
    jaeger_agent_host: str = "localhost"
    jaeger_agent_port: int = 6831

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_ttl_minutes: int = 60

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 1000
    rate_limit_window_seconds: int = 3600

    # File Storage
    document_storage_path: str = "./storage/documents"
    keep_uploaded_documents: bool = False
    archive_jsons: bool = False
    archive_path: str = "./storage/archive"

    # Admin Settings
    admin_username: str = "admin"
    admin_password: str = "change-me-in-production"
    admin_api_key: str = "your-admin-api-key"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_allow_headers: list[str] = ["*"]

    # Billing Configuration
    billing_aggregation_frequency: str = "monthly"
    billing_currency: str = "INR"
    default_rate_per_document: float = 10.00

    # Backup & Archival
    backup_enabled: bool = True
    backup_schedule: str = "0 2 * * 0"
    backup_retention_days: int = 30

    @field_validator(
        "pii_fields",
        "supported_formats",
        "cors_origins",
        "cors_allow_methods",
        "cors_allow_headers",
        mode="before",
    )
    @classmethod
    def parse_list_fields(cls, v: Any) -> Any:
        """Parse list fields from JSON array or comma-separated string."""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            if not v or not v.strip():
                return []
            # Try JSON parsing first
            if v.strip().startswith("["):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Fall back to comma-separated
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    class Config:
        """Pydantic configuration."""

        env_file = str(env_file)
        case_sensitive = False
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


settings = get_settings()
