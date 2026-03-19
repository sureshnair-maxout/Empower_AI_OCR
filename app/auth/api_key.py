"""API Key authentication."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.auth.security import AuthenticationError
from app.core.constants import ErrorCode

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(
    api_key: Optional[str] = Depends(api_key_header),
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

    # TODO: Implement API key verification against database
    # For now, validation stub
    try:
        # Placeholder: In production, query the database for the API key
        org_id = "org-1"  # From database lookup
        if not org_id:
            raise AuthenticationError(
                error_code=ErrorCode.INVALID_API_KEY,
                message="Invalid or revoked API key",
            )
        return {"org_id": org_id, "api_key": api_key}
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
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
