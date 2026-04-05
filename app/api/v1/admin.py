"""Admin endpoints."""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.auth.api_key import verify_api_key
from app.core.config import settings
from app.core.database import get_db
from app.models.database import APIKey, BillingRecord, Document, DocumentType, Organization
from app.schemas.schemas import BillingDashboardResponse

router = APIRouter(prefix="/admin", tags=["Admin"])

OUTPUT_SCHEMA_FILE_MAP = {
    "INVOICE": "invoice.json",
    "AADHAAR_CARD": "aadhaar_card.json",
    "PAN_CARD": "pan_card.json",
    "CHEQUE": "cheque.json",
}


def _load_output_schema_files(org_id: str) -> list[dict[str, Any]]:
    """Load built-in output schemas from config/output_schemas."""
    fallback_items: list[dict[str, Any]] = []
    schema_dir = Path(__file__).resolve().parents[3] / "config" / "output_schemas"

    for code, file_name in OUTPUT_SCHEMA_FILE_MAP.items():
        schema_path = schema_dir / file_name
        if not schema_path.exists():
            continue

        try:
            schema_config = json.loads(schema_path.read_text(encoding="utf-8"))
        except Exception:
            schema_config = {}

        fallback_items.append(
            {
                "id": None,
                "tenant_id": org_id,
                "code": code,
                "name": code.replace("_", " ").title(),
                "description": "Loaded from config/output_schemas",
                "schema_config": schema_config,
                "is_active": True,
                "created_at": None,
                "updated_at": None,
            }
        )

    return fallback_items


class DocumentTypeCreateRequest(BaseModel):
    """Create document type payload."""

    tenant_id: Optional[str] = None
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    schema_config: dict[str, Any]
    is_active: bool = True


async def verify_admin_access(
    auth: dict = Depends(verify_api_key),
    x_admin_key: Optional[str] = Header(default=None, alias="X-Admin-Key"),
) -> dict:
    """Verify caller has admin privileges.

    Supports either:
    - Explicit X-Admin-Key header
    - API key matching admin_api_key
    """
    admin_key = (settings.admin_api_key or "").strip()
    presented_api_key = str(auth.get("api_key") or "")
    api_key_name = str(auth.get("api_key_name") or "")

    if api_key_name.lower() == "admin api key":
        return auth

    if admin_key and admin_key != "your-admin-api-key" and (
        x_admin_key == admin_key or presented_api_key == admin_key
    ):
        return auth

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin privileges required",
    )


@router.get("/dashboard")
async def get_dashboard(
    auth: dict = Depends(verify_admin_access),
    db: AsyncSession = Depends(get_db),
):
    """Get admin dashboard data.

    Args:
        auth: Authentication data from API key.

    Returns:
        Dashboard metrics and data.
    """
    now = datetime.utcnow()
    window_start = now - timedelta(hours=24)
    current_period = now.strftime("%Y-%m")

    total_orgs = (
        await db.execute(select(func.count(Organization.id)).where(Organization.is_active.is_(True)))
    ).scalar_one()
    total_active_keys = (
        await db.execute(select(func.count(APIKey.id)).where(APIKey.is_active.is_(True)))
    ).scalar_one()
    total_documents = (await db.execute(select(func.count(Document.id)))).scalar_one()

    docs_24h = (
        await db.execute(select(func.count(Document.id)).where(Document.created_at >= window_start))
    ).scalar_one()
    completed_24h = (
        await db.execute(
            select(func.count(Document.id)).where(
                Document.created_at >= window_start,
                Document.status == "completed",
            )
        )
    ).scalar_one()
    failed_24h = (
        await db.execute(
            select(func.count(Document.id)).where(
                Document.created_at >= window_start,
                Document.status == "failed",
            )
        )
    ).scalar_one()

    monthly_billing = (
        await db.execute(
            select(func.coalesce(func.sum(BillingRecord.amount), 0.0)).where(
                BillingRecord.billing_period == current_period,
            )
        )
    ).scalar_one()

    top_doc_types_result = await db.execute(
        select(Document.document_type, func.count(Document.id).label("count"))
        .group_by(Document.document_type)
        .order_by(desc("count"))
        .limit(5)
    )
    top_document_types = [
        {"document_type": row[0], "count": int(row[1])} for row in top_doc_types_result.all()
    ]

    recent_failures_result = await db.execute(
        select(
            Document.id,
            Document.org_id,
            Document.file_name,
            Document.error_message,
            Document.updated_at,
        )
        .where(Document.status == "failed")
        .order_by(desc(Document.updated_at))
        .limit(10)
    )
    recent_failures = [
        {
            "document_id": row[0],
            "org_id": row[1],
            "file_name": row[2],
            "error_message": row[3],
            "updated_at": row[4].isoformat() if row[4] else None,
        }
        for row in recent_failures_result.all()
    ]

    success_rate_24h = round((completed_24h / docs_24h) * 100, 2) if docs_24h else 0.0

    return {
        "timestamp": now.isoformat(),
        "deployment_mode": settings.deployment_mode,
        "metrics": {
            "active_organizations": int(total_orgs),
            "active_api_keys": int(total_active_keys),
            "total_documents": int(total_documents),
            "documents_last_24h": int(docs_24h),
            "failed_last_24h": int(failed_24h),
            "success_rate_last_24h": success_rate_24h,
            "monthly_billing_total": float(monthly_billing or 0.0),
            "current_billing_period": current_period,
        },
        "top_document_types": top_document_types,
        "recent_failures": recent_failures,
        "requested_by_org": auth.get("org_id"),
    }


@router.get("/billing")
async def get_billing_dashboard(
    tenant_id: str,
    auth: dict = Depends(verify_admin_access),
    db: AsyncSession = Depends(get_db),
) -> BillingDashboardResponse:
    """Get billing dashboard for a tenant.

    Args:
        tenant_id: Tenant ID.
        auth: Authentication data from API key.

    Returns:
        Billing dashboard data.
    """
    current_period = datetime.utcnow().strftime("%Y-%m")

    monthly_total = (
        await db.execute(
            select(func.coalesce(func.sum(BillingRecord.amount), 0.0)).where(
                BillingRecord.org_id == tenant_id,
                BillingRecord.billing_period == current_period,
            )
        )
    ).scalar_one()

    document_count = (
        await db.execute(
            select(func.count(BillingRecord.id)).where(
                BillingRecord.org_id == tenant_id,
                BillingRecord.billing_period == current_period,
            )
        )
    ).scalar_one()

    breakdown_rows = (
        await db.execute(
            select(
                BillingRecord.document_type,
                func.count(BillingRecord.id).label("count"),
                func.coalesce(func.sum(BillingRecord.amount), 0.0).label("amount"),
            )
            .where(
                BillingRecord.org_id == tenant_id,
                BillingRecord.billing_period == current_period,
            )
            .group_by(BillingRecord.document_type)
            .order_by(desc("amount"))
        )
    ).all()

    breakdown_by_type = {
        row[0]: {"count": int(row[1]), "amount": float(row[2] or 0.0)} for row in breakdown_rows
    }

    trend_rows = (
        await db.execute(
            select(
                BillingRecord.billing_period,
                func.count(BillingRecord.id).label("count"),
                func.coalesce(func.sum(BillingRecord.amount), 0.0).label("amount"),
            )
            .where(BillingRecord.org_id == tenant_id)
            .group_by(BillingRecord.billing_period)
            .order_by(desc(BillingRecord.billing_period))
            .limit(6)
        )
    ).all()

    trend_data = [
        {
            "billing_period": row[0],
            "document_count": int(row[1]),
            "total_amount": float(row[2] or 0.0),
        }
        for row in reversed(trend_rows)
    ]

    return BillingDashboardResponse(
        current_period=current_period,
        monthly_total=float(monthly_total or 0.0),
        document_count=int(document_count),
        breakdown_by_type=breakdown_by_type,
        trend_data=trend_data,
    )


@router.get("/document-types")
async def list_document_types(
    tenant_id: Optional[str] = None,
    include_inactive: bool = False,
    auth: dict = Depends(verify_admin_access),
    db: AsyncSession = Depends(get_db),
):
    """List document type schemas."""
    org_id = tenant_id or str(auth.get("org_id"))

    try:
        query = select(DocumentType).where(DocumentType.org_id == org_id)
        if not include_inactive:
            query = query.where(DocumentType.is_active.is_(True))

        query = query.order_by(DocumentType.code)
        results = (await db.execute(query)).scalars().all()

        payload = []
        for row in results:
            try:
                schema_config = json.loads(row.schema_config or "{}")
            except json.JSONDecodeError:
                schema_config = {}
            payload.append(
                {
                    "id": row.id,
                    "tenant_id": row.org_id,
                    "code": row.code,
                    "name": row.name,
                    "description": row.description,
                    "schema_config": schema_config,
                    "is_active": row.is_active,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                    "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                }
            )

        filesystem_items = _load_output_schema_files(org_id)

        if not payload:
            return {
                "count": len(filesystem_items),
                "items": filesystem_items,
                "source": "filesystem_default",
                "warning": "No document_types rows found; returned built-in schema files",
            }

        existing_codes = {str(item.get("code") or "").upper() for item in payload}
        for item in filesystem_items:
            if str(item.get("code") or "").upper() not in existing_codes:
                payload.append(item)

        return {"count": len(payload), "items": payload, "source": "database+filesystem"}
    except SQLAlchemyError as exc:
        fallback_items = _load_output_schema_files(org_id)

        return {
            "count": len(fallback_items),
            "items": fallback_items,
            "source": "filesystem_fallback",
            "warning": "Database document_types unavailable; returned schema files instead",
            "db_error": str(exc),
        }


@router.post("/document-types")
async def create_document_type(
    request: DocumentTypeCreateRequest,
    auth: dict = Depends(verify_admin_access),
    db: AsyncSession = Depends(get_db),
):
    """Create a new document type schema.

    Args:
        auth: Authentication data from API key.

    Returns:
        Created document type.
    """
    org_id = request.tenant_id or str(auth.get("org_id"))
    code = request.code.strip().upper()

    existing = (
        await db.execute(
            select(DocumentType.id).where(
                DocumentType.org_id == org_id,
                DocumentType.code == code,
            )
        )
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Document type '{code}' already exists for tenant {org_id}",
        )

    row = DocumentType(
        org_id=org_id,
        code=code,
        name=request.name.strip(),
        description=request.description,
        schema_config=json.dumps(request.schema_config, ensure_ascii=False),
        is_active=request.is_active,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)

    return {
        "id": row.id,
        "tenant_id": row.org_id,
        "code": row.code,
        "name": row.name,
        "description": row.description,
        "schema_config": request.schema_config,
        "is_active": row.is_active,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }
