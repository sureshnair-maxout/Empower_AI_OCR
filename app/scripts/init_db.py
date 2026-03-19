"""Initialize database with default data."""

import logging
import hashlib
import uuid
from datetime import datetime

from app.core.database import SyncSessionLocal
from app.models.database import Organization, APIKey
import secrets

logger = logging.getLogger(__name__)


def hash_api_key(api_key: str) -> str:
    """Hash API key using SHA256."""
    return hashlib.sha256(api_key.encode()).hexdigest()


def create_default_organization():
    """Create default organization for owner mode."""
    db = SyncSessionLocal()
    try:
        # Check if organization exists
        existing_org = db.query(Organization).filter(
            Organization.name == "Default Organization"
        ).first()

        if existing_org:
            logger.info("Default organization already exists")
            return existing_org

        # Create default organization
        org = Organization(
            id=str(uuid.uuid4()),
            name="Default Organization",
            description="Default organization for single-tenant setup",
            is_active=True,
            deployment_mode="owner",
            billing_enabled=False,
            data_localization=True,
            enforce_pii=True,
        )
        db.add(org)
        db.commit()
        db.refresh(org)

        logger.info(f"Created default organization: {org.id}")

        # Create default API key
        api_key = secrets.token_urlsafe(20)
        api_key_obj = APIKey(
            id=str(uuid.uuid4()),
            org_id=org.id,
            key_hash=hash_api_key(api_key),
            name="Default API Key",
            is_active=True,
        )
        db.add(api_key_obj)
        db.commit()

        logger.info(f"Created default API key")
        logger.warning(f"Save this API key securely: {api_key}")

        return org

    except Exception as e:
        logger.error(f"Failed to create default organization: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Initialize database."""
    logger.info("Initializing database...")

    try:
        create_default_organization()
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    main()
