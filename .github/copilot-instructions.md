<!-- Copilot Custom Instructions for Empower AI OCR Workspace -->

## Project Overview

This is a production-grade OCR (Optical Character Recognition) API built with FastAPI, designed to integrate with ERP systems. It features:

- Multi-tenant SaaS architecture with single-tenant owner mode
- LLM-powered document processing (Ollama GLM-OCR, SGLang)
- Comprehensive authentication and authorization
- Billing and usage tracking module
- India compliance (PII handling, data localization)
- OpenTelemetry observability
- Docker containerization
- PostgreSQL + Redis infrastructure

## Architecture Principles

1. **Abstraction**: LLM layer is abstracted for easy provider switching
2. **Multi-Tenancy**: Context-based tenant isolation at all layers
3. **Security**: API key + JWT authentication with role-based access
4. **Observability**: Structured logging, OpenTelemetry tracing, metrics
5. **Compliance**: PII detection/masking, data localization, audit logging
6. **Scalability**: Async operations, connection pooling, stateless design

## Project Structure

```
app/
├── api/v1/              # API endpoints (OCR, tenancy, admin)
├── auth/                # Authentication (API keys, JWT, security)
├── billing/             # Billing and usage tracking
├── core/                # Configuration and database setup
├── llm/                 # LLM abstraction layer (providers: Ollama, SGLang)
├── models/              # SQLAlchemy database models
├── observability/       # OpenTelemetry setup
├── schemas/             # Pydantic request/response models
├── services/            # Business logic (OCR, billing, tenancy)
├── tenancy/             # Multi-tenancy context management
├── scripts/             # Utility scripts (DB init, migrations)
└── main.py              # FastAPI application entry point

config/                  # Configuration files (document types YAML)
docker/                  # Docker and Docker Compose files
docs/                    # Documentation (API, setup, deployment)
tests/                   # Unit and integration tests
```

## Key Technologies

- **Framework**: FastAPI with Uvicorn
- **Database**: PostgreSQL with SQLAlchemy ORM (async)
- **Cache**: Redis
- **Authentication**: JWT + API Key
- **LLM Provider**: Ollama (with GLM-OCR model)
- **Observability**: OpenTelemetry + Jaeger
- **Containerization**: Docker + Docker Compose
- **Task Runner**: Alembic for migrations

## Development Guidelines

### When Adding New Features

1. **API Endpoints**: Create router in `app/api/v1/`
2. **Business Logic**: Add service class in `app/services/`
3. **Database Model**: Add SQLAlchemy model in `app/models/database.py`
4. **Request/Response**: Add Pydantic schema in `app/schemas/schemas.py`
5. **Tests**: Create test file in `tests/`
6. **Documentation**: Update relevant docs in `docs/`

### Environment Setup

Create `.env` from `.env.example`:
```
APP_ENV=development
DATABASE_URL=postgresql://ocr_user:ocr_password@localhost:5432/ocr_db
OLLAMA_BASE_URL=http://localhost:11434
LLM_PROVIDER=ollama
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=<32-char-random-key>
```

### Important Configuration

- **Mode**: `DEPLOYMENT_MODE` (tenant/owner) controls multi-tenancy features
- **Billing**: `ENABLE_BILLING` activates billing module (requires DEPLOYMENT_MODE=tenant)
- **Compliance**: `ENFORCE_PII_HANDLING` masks sensitive data
- **Logging**: `LOG_FORMAT=json` for structured logging

### Common Commands

```bash
# Setup environment
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Database
alembic upgrade head                          # Apply migrations
alembic revision --autogenerate -m "msg"     # Create migration
python -m app.scripts.init_db                # Initialize with defaults

# Run application
uvicorn app.main:app --reload                # Development
python app/main.py                           # Quick start

# Run tests
pytest                                       # All tests
pytest tests/test_ocr_service.py -v         # Specific test
pytest --cov=app                             # With coverage

# Docker
docker-compose -f docker/docker-compose.yml up -d
docker-compose -f docker/docker-compose.yml logs -f api
```

## Important Notes

1. **Multi-Tenancy**: Always filter queries by `org_id` using `TenantFilter`
2. **Error Codes**: Use constants from `app/core/constants.py` for consistency
3. **Logging**: Use structured JSON logging with request IDs for correlation
4. **Security**: Never log sensitive data (API keys, PII); use masking
5. **Async**: Prefer async/await patterns for I/O operations
6. **Database**: Use SQLAlchemy async sessions from `app/core/database.py`

## File Locations Reference

| Purpose | Path |
|---------|------|
| Configuration | `app/core/config.py` |
| Constants & Enums | `app/core/constants.py` |
| Database Models | `app/models/database.py` |
| Schemas | `app/schemas/schemas.py` |
| LLM Base | `app/llm/base.py` |
| Ollama Provider | `app/llm/providers/ollama.py` |
| Environment | `.env` (from `.env.example`) |
| Document Types | `config/document_types.yaml` |
| Docker Config | `docker/docker-compose.yml` |
| Setup Guide | `docs/SETUP.md` |
| API Docs | `docs/API.md` |
| LLM Guide | `docs/LLM_CONFIGURATION.md` |
| Deployment | `docs/DEPLOYMENT.md` |
| Architecture | `docs/ARCHITECTURE.md` |

## Next Steps After Folder Creation

The foundational application structure is now in place. Next phase should focus on:

1. **Core Implementation** - Complete OCR processing pipeline
2. **Endpoint Implementation** - Fully implement all API endpoints
3. **Database Integration** - Implement data access layer
4. **Testing** - Comprehensive unit and integration tests
5. **Admin Dashboard** - Web UI for tenant management
6. **Documentation** - API examples and tutorials
7. **Performance** - Load testing and optimization
8. **Security** - Penetration testing and audit

## Support & Resources

- **Setup**: Read `docs/SETUP.md` for detailed local setup
- **API Usage**: See `docs/API.md` for endpoint documentation
- **LLM Setup**: Check `docs/LLM_CONFIGURATION.md` for model configuration
- **Deployment**: Review `docs/DEPLOYMENT.md` for production deployment
- **Architecture**: See `docs/ARCHITECTURE.md` for system design

