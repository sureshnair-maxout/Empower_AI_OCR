"""Multi-tenancy context management."""

from contextvars import ContextVar
from typing import Optional

from fastapi import Depends, HTTPException, status

org_context: ContextVar[Optional[str]] = ContextVar("org_id", default=None)


def set_org_context(org_id: str) -> None:
    """Set the current organization context.

    Args:
        org_id: Organization ID.
    """
    org_context.set(org_id)


def get_org_context() -> Optional[str]:
    """Get the current organization context.

    Returns:
        Current organization ID or None.
    """
    return org_context.get()


async def get_current_org() -> str:
    """Dependency to get current organization.

    Returns:
        Current organization ID.

    Raises:
        HTTPException: If org context is not set.
    """
    org_id = get_org_context()
    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Organization context not set",
        )
    return org_id


class TenantFilter:
    """SQLAlchemy filter for multi-tenancy."""

    @staticmethod
    def filter_by_org(query, model, org_id: str):
        """Add organization filter to query.

        Args:
            query: SQLAlchemy query object.
            model: Model class with org_id field.
            org_id: Organization ID to filter by.

        Returns:
            Filtered query.
        """
        if hasattr(model, "org_id"):
            return query.filter(model.org_id == org_id)
        return query
