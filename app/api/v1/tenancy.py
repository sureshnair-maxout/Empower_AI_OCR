"""Tenancy management endpoints (admin only)."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.api_key import verify_api_key
from app.schemas.schemas import OrganizationCreate, OrganizationResponse

router = APIRouter()


@router.post("/tenants", response_model=OrganizationResponse)
async def create_tenant(
    org_data: OrganizationCreate,
    auth: dict = Depends(verify_api_key),
):
    """Create a new tenant/organization.

    Args:
        org_data: Organization creation data.
        auth: Authentication data from API key.

    Returns:
        Created organization.
    """
    # TODO: Check if caller is admin
    # TODO: Validate organization name uniqueness
    # TODO: Create organization in database
    # TODO: Create default API key
    # TODO: Emit audit log

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint not yet implemented",
    )


@router.get("/tenants/{tenant_id}", response_model=OrganizationResponse)
async def get_tenant(
    tenant_id: str,
    auth: dict = Depends(verify_api_key),
):
    """Get tenant details.

    Args:
        tenant_id: Tenant ID.
        auth: Authentication data from API key.

    Returns:
        Organization details.
    """
    # TODO: Check if caller has permission
    # TODO: Query database
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint not yet implemented",
    )
