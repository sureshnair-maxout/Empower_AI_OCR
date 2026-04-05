"""Initialize database with default data."""

import logging
import hashlib
import uuid

from app.core.config import settings
from app.core.database import Base, SyncSessionLocal, sync_engine
from app.models.database import Organization, APIKey
import secrets

logger = logging.getLogger(__name__)


def hash_api_key(api_key: str) -> str:
    """Hash API key using SHA256."""
    return hashlib.sha256(api_key.encode()).hexdigest()


def ensure_tables() -> None:
    """Create database tables if they do not exist."""
    Base.metadata.create_all(bind=sync_engine)
    logger.info("Database tables verified/created")


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
            _ensure_seed_keys(db=db, org_id=existing_org.id)
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

        _ensure_seed_keys(db=db, org_id=org.id)

        return org

    except Exception as e:
        logger.error(f"Failed to create default organization: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def _ensure_seed_keys(db, org_id: str) -> None:
    """Ensure default and admin API keys exist for initial bootstrap."""
    default_key_name = "Default API Key"
    existing_default = db.query(APIKey).filter(
        APIKey.org_id == org_id,
        APIKey.name == default_key_name,
        APIKey.is_active.is_(True),
    ).first()

    if not existing_default:
        default_api_key = secrets.token_urlsafe(20)
        db.add(
            APIKey(
                id=str(uuid.uuid4()),
                org_id=org_id,
                key_hash=hash_api_key(default_api_key),
                name=default_key_name,
                is_active=True,
            )
        )
        db.commit()
        logger.info("Created default API key")
        logger.warning("Save this API key securely: %s", default_api_key)

    admin_key_name = "Admin API Key"
    configured_admin_key = (settings.admin_api_key or "").strip()
    existing_admin = db.query(APIKey).filter(
        APIKey.org_id == org_id,
        APIKey.name == admin_key_name,
        APIKey.is_active.is_(True),
    ).first()

    if configured_admin_key and configured_admin_key != "your-admin-api-key" and not existing_admin:
        db.add(
            APIKey(
                id=str(uuid.uuid4()),
                org_id=org_id,
                key_hash=hash_api_key(configured_admin_key),
                name=admin_key_name,
                is_active=True,
            )
        )
        db.commit()
        logger.info("Seeded admin API key from ADMIN_API_KEY")


def main():
    """Initialize database."""
    logger.info("Initializing database...")

    try:
        ensure_tables()
        create_default_organization()
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    main()
