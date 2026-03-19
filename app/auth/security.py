"""Authentication and security utilities."""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings
from app.core.constants import ErrorCode

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    """Token payload data."""

    sub: str  # Subject (user ID or API key ID)
    org_id: Optional[str] = None
    exp: Optional[datetime] = None
    type: str = "access"  # access or refresh


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    org_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({
        "exp": expire,
        "org_id": org_id,
        "type": "access",
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def create_refresh_token(
    data: dict,
    org_id: Optional[str] = None,
) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)

    to_encode.update({
        "exp": expire,
        "org_id": org_id,
        "type": "refresh",
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        subject: str = payload.get("sub")
        org_id: Optional[str] = payload.get("org_id")
        token_type: str = payload.get("type", "access")

        if subject is None:
            return None

        return TokenData(
            sub=subject,
            org_id=org_id,
            type=token_type,
        )
    except JWTError:
        return None


class AuthenticationError(Exception):
    """Authentication error."""

    def __init__(
        self,
        error_code: ErrorCode = ErrorCode.INVALID_API_KEY,
        message: str = "Authentication failed",
        details: Optional[str] = None,
    ):
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(self.message)


class AuthorizationError(Exception):
    """Authorization error."""

    def __init__(
        self,
        error_code: ErrorCode = ErrorCode.INSUFFICIENT_PERMISSIONS,
        message: str = "Insufficient permissions",
        details: Optional[str] = None,
    ):
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(self.message)
