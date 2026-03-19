"""Database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Create async engine for async operations
async_engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_size=settings.database_pool_size,
    max_overflow=10,
    pool_pre_ping=True,
)

# Build a sync DB URL for sync engine (use psycopg2 driver)
if "+asyncpg" in settings.database_url:
    sync_db_url = settings.database_url.replace("+asyncpg", "+psycopg2")
else:
    sync_db_url = settings.database_url.replace("postgresql", "postgresql+psycopg2", 1)

sync_engine = create_engine(
    sync_db_url,
    echo=settings.database_echo,
    pool_size=settings.database_pool_size,
)

# Session factory for async sessions
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Session factory for sync sessions
SyncSessionLocal = sessionmaker(
    sync_engine,
    expire_on_commit=False,
    autocommit=False,
)

# Declarative base for models
Base = declarative_base()


async def get_db():
    """Dependency for getting async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_db():
    """Dependency for getting sync database session."""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
