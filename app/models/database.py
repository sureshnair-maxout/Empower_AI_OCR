"""Database models for OCR application."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Boolean, Float, Integer, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class Organization(Base):
    """Organization/Tenant model."""

    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    deployment_mode = Column(String(20), default="tenant")  # tenant or owner
    billing_enabled = Column(Boolean, default=True)
    data_localization = Column(Boolean, default=True)
    enforce_pii = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    api_keys = relationship("APIKey", back_populates="organization", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="organization", cascade="all, delete-orphan")
    billing_records = relationship(
        "BillingRecord", back_populates="organization", cascade="all, delete-orphan"
    )


class APIKey(Base):
    """API Key model for authentication."""

    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="api_keys")
    __table_args__ = (Index("idx_org_id_active", "org_id", "is_active"),)


class Document(Base):
    """Document processing record."""

    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)
    document_type = Column(String(50), nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="documents")
    ocr_result = relationship("OCRResult", uselist=False, back_populates="document")
    __table_args__ = (
        Index("idx_org_id_document_type", "org_id", "document_type"),
        Index("idx_org_id_created_at", "org_id", "created_at"),
    )


class OCRResult(Base):
    """OCR processing result."""

    __tablename__ = "ocr_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, unique=True)
    request_id = Column(String(36), nullable=False)
    extracted_data = Column(Text, nullable=True)  # JSON stored as text
    confidence_score = Column(Float, default=0.0)
    processing_time_ms = Column(Integer, nullable=True)
    model_version = Column(String(50), nullable=True)
    warnings = Column(Text, nullable=True)  # JSON array as text
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    document = relationship("Document", back_populates="ocr_result")


class DocumentType(Base):
    """Document type schema definition."""

    __tablename__ = "document_types"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    schema_config = Column(Text, nullable=False)  # JSON schema as text
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BillingRecord(Base):
    """Billing and usage tracking record."""

    __tablename__ = "billing_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=True)
    document_type = Column(String(50), nullable=False)
    rate_per_document = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    billing_period = Column(String(7), nullable=False)  # YYYY-MM format
    status = Column(String(20), default="pending")  # pending, invoiced, paid
    created_at = Column(DateTime, default=datetime.utcnow)
    used_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="billing_records")
    __table_args__ = (
        Index("idx_org_id_billing_period", "org_id", "billing_period"),
        Index("idx_org_id_used_date", "org_id", "used_date"),
    )


class AuditLog(Base):
    """Audit log for compliance and security."""

    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)  # JSON details
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        Index("idx_org_id_action", "org_id", "action"),
        Index("idx_audit_log_org_created", "org_id", "created_at"),
    )
