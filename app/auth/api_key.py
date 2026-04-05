"""API Key authentication."""

import hashlib
from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import AuthenticationError
from app.core.constants import ErrorCode
from app.core.database import get_db
from app.models.database import APIKey, Organization

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(
    api_key: Optional[str] = Depends(api_key_header),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Verify API key from header.

    Returns:
        Dictionary with org_id and other metadata if valid.

    Raises:
        HTTPException: If API key is invalid or missing.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    try:
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        api_key_row = (
            await db.execute(
                select(APIKey).where(
                    APIKey.key_hash == key_hash,
                    APIKey.is_active.is_(True),
                )
            )
        ).scalar_one_or_none()

        if not api_key_row:
            raise AuthenticationError(
                error_code=ErrorCode.INVALID_API_KEY,
                message="Invalid or revoked API key",
            )

        org_row = (
            await db.execute(
                select(Organization).where(
                    Organization.id == api_key_row.org_id,
                    Organization.is_active.is_(True),
                )
            )
        ).scalar_one_or_none()

        if not org_row:
            raise AuthenticationError(
                error_code=ErrorCode.TENANT_DISABLED,
                message="Organization not found or disabled",
            )

        api_key_row.last_used = datetime.utcnow()
        await db.commit()

        return {
            "org_id": org_row.id,
            "org_name": org_row.name,
            "api_key_id": api_key_row.id,
            "api_key_name": api_key_row.name,
            "api_key": api_key,
        }
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable while validating API key",
        )


class APIKeyValidator:
    """Validator for API keys."""

    def __init__(self):
        """Initialize validator."""
        self.cache: dict = {}  # TODO: Replace with Redis cache

    async def validate(self, api_key: str) -> Optional[dict]:
        """Validate an API key.

        Args:
            api_key: The API key to validate.

        Returns:
            Dictionary with org_id and metadata if valid, None otherwise.
        """
        # Check cache first
        if api_key in self.cache:
            return self.cache[api_key]

        # TODO: Query database for API key validation
        # Check if key is active and not revoked
        # Store in cache with TTL

        return None
