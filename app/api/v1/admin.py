"""Admin endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.api_key import verify_api_key
from app.schemas.schemas import BillingDashboardResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
async def get_dashboard(auth: dict = Depends(verify_api_key)):
    """Get admin dashboard data.

    Args:
        auth: Authentication data from API key.

    Returns:
        Dashboard metrics and data.
    """
    # TODO: Check if caller is admin
    # TODO: Aggregate system metrics
    # TODO: Get usage statistics
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint not yet implemented",
    )


@router.get("/billing")
async def get_billing_dashboard(
    tenant_id: str,
    auth: dict = Depends(verify_api_key),
) -> BillingDashboardResponse:
    """Get billing dashboard for a tenant.

    Args:
        tenant_id: Tenant ID.
        auth: Authentication data from API key.

    Returns:
        Billing dashboard data.
    """
    # TODO: Check if caller has permission
    # TODO: Query billing records
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint not yet implemented",
    )


@router.post("/document-types")
async def create_document_type(auth: dict = Depends(verify_api_key)):
    """Create a new document type schema.

    Args:
        auth: Authentication data from API key.

    Returns:
        Created document type.
    """
    # TODO: Validate schema
    # TODO: Store in database
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint not yet implemented",
    )
