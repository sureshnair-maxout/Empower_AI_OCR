"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.observability.telemetry import setup_otel

# Import routers
from app.api.v1 import ocr
from app.api.v1.sandbox import router as sandbox_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}...")
    # Pass the FastAPI app instance so instrumentation can attach correctly
    setup_otel(app)
    yield
    # Shutdown
    print(f"Shutting down {settings.app_name}...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Production-grade OCR API with LLM integration and multi-tenancy",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "app": settings.app_name,
            "version": settings.app_version,
            "environment": settings.app_env,
        },
    )


# API v1 routes
# Health router intentionally not exposed separately (root /health exists)
app.include_router(ocr.router, prefix=settings.api_prefix, tags=["OCR"])
app.include_router(sandbox_router)
# app.include_router(tenancy.router, prefix=settings.api_prefix, tags=["Tenancy"])
# app.include_router(admin.router, prefix=settings.api_prefix, tags=["Admin"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        access_log=True,
    )
