# Empower AI OCR API

A production-grade OCR API that integrates with ERP systems, featuring advanced document processing with LLM-based OCR, multi-tenant support, and comprehensive billing capabilities.

## Features

### Core Capabilities
- **Document OCR**: Support for Invoice, Cheque, PAN Card, Aadhaar Card with GLM-OCR on Ollama
- **Structured Output**: JSON responses with field-level confidence scores and data type information
- **Document Type Management**: Configurable document type schemas with predefined field mappings
- **Real-time ERP Integration**: REST API with real-time push to ERP systems
- **Error Handling**: Intuitive error messages for document type mismatches and processing failures

### Architecture Highlights
- **LLM Abstraction Layer**: Easily switch between Ollama, SGLang, or other providers without code changes
- **Multi-Tenancy**: Support for multiple organizations with isolated data
- **Dual Deployment Modes**:
  - **Tenant Mode**: Full multi-tenancy with billing and usage tracking
  - **Owner Mode**: Single-tenant deployment without billing overhead
- **India Compliance**: Built-in support for data localization and PII handling (Aadhaar, PAN)
- **Comprehensive Security**: API key authentication, role-based access control (RBAC)
- **Observability**: OpenTelemetry integration for distributed tracing and monitoring
- **Containerization**: Docker and Docker Compose for easy deployment

### Admin Features
- Tenant management (CRUD operations)
- API key generation and management
- Document type configuration management
- Usage analytics and billing dashboard
- LLM model monitoring and performance metrics
- Audit logs and compliance reporting

## Project Structure

```
empower-ai-ocr/
├── app/
│   ├── api/                 # API endpoints (v1 routes)
│   ├── core/                # Core configuration, constants
│   ├── models/              # SQLAlchemy database models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic layer
│   ├── llm/                 # LLM provider abstraction
│   ├── auth/                # Authentication & authorization
│   ├── tenancy/             # Multi-tenancy layer
│   ├── billing/             # Billing & usage tracking
│   ├── observability/       # OpenTelemetry setup
│   └── main.py              # FastAPI application entry point
├── config/
│   ├── document_types.yaml  # Document type schemas
│   ├── settings.py          # Configuration management
│   └── database.py          # Database setup
├── tests/                   # Unit and integration tests
├── docker/
│   ├── Dockerfile           # Application container
│   ├── docker-compose.yml   # Full stack orchestration
│   └── nginx.conf           # Reverse proxy configuration (optional)
├── docs/
│   ├── API.md               # API documentation
│   ├── SETUP.md             # Setup instructions
│   ├── LLM_CONFIGURATION.md # LLM provider configuration
│   └── DEPLOYMENT.md        # Deployment guides
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Ollama with GLM-OCR model
- Docker & Docker Compose (for containerized deployment)

### Local Development Setup

1. **Clone the repository**
```bash
cd "d:\Empower_AI_OCR"
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Initialize database**
```bash
alembic upgrade head
python -m app.scripts.init_db
```

5. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Access the API**
- API Documentation: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/api/v1/health

### Docker Deployment

```bash
docker-compose -f docker/docker-compose.yml up -d
```

This will start:
- API Server (Port 8000)
- PostgreSQL Database (Port 5432)
- Redis Cache (Port 6379)
- Jaeger Tracing (Port 16686)

## Configuration

### Environment Modes

#### Tenant Mode (Multi-Tenant SaaS)
```
DEPLOYMENT_MODE=tenant
ENABLE_BILLING=true
```
- Multiple organizations supported
- Usage tracking and billing
- Isolated data per tenant
- Admin dashboard for all tenants

#### Owner Mode (Single Tenant)
```
DEPLOYMENT_MODE=owner
ENABLE_BILLING=false
```
- Single organization only
- No billing overhead
- Simplified configuration
- Reduced database schema

### LLM Provider Configuration

See [docs/LLM_CONFIGURATION.md](docs/LLM_CONFIGURATION.md) for detailed instructions on:
- Configuring Ollama with GLM-OCR
- Switching to alternative providers (SGLang, etc.)
- Model versioning and fallback strategies
- Performance tuning

### Document Types

Document type schemas are defined in [config/document_types.yaml](config/document_types.yaml). Each document type specifies:
- Required and optional fields
- Field data types
- Validation rules
- Confidence thresholds

## API Usage

### Authentication
All API requests require an API key:
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/...
```

### OCR Document Endpoint

**Request:**
```bash
POST /api/v1/ocr/process
Content-Type: multipart/form-data

{
  "document_image": <binary>,
  "document_type_code": "INVOICE"
}
```

**Response:**
```json
{
  "request_id": "uuid",
  "document_type": "INVOICE",
  "status": "success",
  "ocr_results": {
    "invoice_number": {
      "value": "INV-2024-001",
      "confidence": 0.98,
      "data_type": "string",
      "required": true
    },
    "invoice_date": {
      "value": "2024-02-26",
      "confidence": 0.95,
      "data_type": "date",
      "required": true
    },
    "total_amount": {
      "value": "50000.00",
      "confidence": 0.92,
      "data_type": "decimal",
      "required": true
    }
  },
  "warnings": [],
  "erp_payload": {...}
}
```

### Error Handling

```json
{
  "error_code": "DOCUMENT_TYPE_MISMATCH",
  "message": "Uploaded document does not match specified type 'PAN_CARD'",
  "details": "Document appears to be a CHEQUE based on OCR analysis",
  "request_id": "uuid"
}
```

## Security

### Authentication Methods
- **API Key**: For service-to-service authentication
- **JWT Tokens**: For user/admin sessions
- **OAuth 2.0**: (Future) For third-party integrations

### Data Protection
- PII field encryption at rest
- Aadhaar/PAN number masking in logs
- India data localization enforcement
- Audit logging for all sensitive operations
- Document auto-deletion after processing

## Observability

### OpenTelemetry Integration
- Request/response tracing
- Database query monitoring
- LLM API call tracking
- Performance metrics
- Jaeger UI for visualization (http://localhost:16686)

### Logs
- JSON-formatted structured logs
- Request ID correlation across services
- PII redaction in log output

## Admin Features

Access admin dashboard at: http://localhost:8000/admin

### Tenant Management
- Create/update/delete organizations
- Configure per-tenant settings
- View usage metrics

### API Key Management
- Generate and revoke API keys
- Set rate limits per key
- Track key usage

### Document Type Management
- CRUD operations for document types
- Schema validation and testing
- Version management

### Billing & Usage
- Real-time usage metrics
- Monthly billing aggregation
- Payment tracking (owner mode: disabled)
- Usage reports and analytics

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app

# Specific test file
pytest tests/test_ocr_service.py -v
```

## Development

### Code Style
```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8 .

# Type checking
mypy app/
```

## Documentation

- [API Documentation](docs/API.md) - Detailed API reference
- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [LLM Configuration](docs/LLM_CONFIGURATION.md) - Model setup and switching
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please reach out to support@empowerai.com

## Roadmap

- [ ] OAuth 2.0 integration
- [ ] Advanced ML model comparison
- [ ] Webhook support for async processing
- [ ] Mobile SDK
- [ ] Advanced analytics dashboard
- [ ] Machine learning model versioning and A/B testing
