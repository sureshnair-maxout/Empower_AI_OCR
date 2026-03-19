# Setup Guide - Empower AI OCR

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Setup](#docker-setup)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [LLM Provider Setup](#llm-provider-setup)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

## Local Development Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 6+
- Ollama with GLM-OCR model
- Git

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd "Empower_AI_OCR"
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt

# For development
pip install -e ".[dev]"
```

### Step 4: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Application
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-min-32-chars-change-in-production

# Database (update with your credentials)
DATABASE_URL=postgresql://ocr_user:ocr_password@localhost:5432/ocr_db

# LLM
OLLAMA_BASE_URL=http://localhost:11434
OCR_MODEL_NAME=glm-ocr

# Redis
REDIS_URL=redis://localhost:6379/0

# Admin
ADMIN_API_KEY=generate-a-random-key
```

### Step 5: Setup Database

```bash
# Install Alembic (for migrations)
pip install alembic

# Initialize migrations directory (if not exists)
alembic init -t async migrations

# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### Step 6: Initialize Data

```bash
# Create initial admin user and organization
python -m app.scripts.init_db

# (Or manually)
python -c "from app.scripts.init_db import main; import asyncio; asyncio.run(main())"
```

### Step 7: Start Ollama

In a separate terminal:

```bash
ollama serve
```

If GLM-OCR is not installed:

```bash
ollama pull glm-ocr
```

### Step 8: Run Application

```bash
# Development with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Step 9: Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# API documentation
# Open http://localhost:8000/docs in browser
```

## Docker Setup

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### Quick Start

```bash
# From project root
docker-compose -f docker/docker-compose.yml up -d

# Check status
docker-compose -f docker/docker-compose.yml ps

# View logs
docker-compose -f docker/docker-compose.yml logs -f api
```

### Services

After startup, the following services are available:

| Service | URL | Purpose |
|---------|-----|---------|
| API | http://localhost:8000 | OCR API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| PostgreSQL | localhost:5432 | Database |
| Redis | localhost:6379 | Cache |
| Jaeger | http://localhost:16686 | Tracing & Monitoring |

### Database Migrations in Docker

```bash
# Run migrations
docker-compose exec api alembic upgrade head

# Create migration
docker-compose exec api alembic revision --autogenerate -m "Migration name"
```

### Stop Services

```bash
docker-compose down

# With data cleanup
docker-compose down -v
```

## Configuration

### Environment Variables

Create `.env` file with the following:

```env
# Application Settings
APP_NAME=Empower AI OCR API
APP_VERSION=1.0.0
APP_ENV=development
API_PREFIX=/api/v1
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
DEBUG=true

# Mode Settings
DEPLOYMENT_MODE=tenant  # or "owner"
ENABLE_BILLING=true

# Database
DATABASE_URL=postgresql://ocr_user:ocr_password@localhost:5432/ocr_db
DATABASE_POOL_SIZE=10
DATABASE_ECHO=false

# Authentication
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256

# India Compliance
DATA_LOCALIZATION_ENABLED=true
ENFORCE_PII_HANDLING=true

# LLM / Ollama
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OCR_MODEL_NAME=glm-ocr
OCR_MODEL_VERSION=latest
LLM_TIMEOUT_SECONDS=120
LLM_MAX_RETRIES=3

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_TTL_MINUTES=60

# Observability
OTEL_ENABLED=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
JAEGER_ENABLED=false
JAEGER_AGENT_HOST=localhost
JAEGER_AGENT_PORT=6831

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# File Storage
DOCUMENT_STORAGE_PATH=./storage/documents
KEEP_UPLOADED_DOCUMENTS=false

# Admin
ADMIN_USERNAME=admin
ADMIN_API_KEY=change-me-in-production
```

### File Storage

Create storage directories:

```bash
mkdir -p storage/documents storage/archive logs
chmod 755 storage logs
```

## Database Setup

### PostgreSQL Local Setup

```bash
# macOS
brew install postgresql
brew services start postgresql

# Linux (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

### Create Database User

```bash
# Connect to PostgreSQL
psql -U postgres

# Create user and database
CREATE USER ocr_user WITH PASSWORD 'ocr_password';
CREATE DATABASE ocr_db OWNER ocr_user;
GRANT ALL PRIVILEGES ON DATABASE ocr_db TO ocr_user;
\q
```

### Verify Connection

```bash
psql -U ocr_user -d ocr_db -h localhost
```

## LLM Provider Setup

### Ollama Setup

```bash
# 1. Download Ollama
curl https://ollama.ai/install.sh | sh

# 2. Start Ollama server
ollama serve

# 3. In another terminal, pull the model
ollama pull glm-ocr

# 4. Verify model is loaded
curl http://localhost:11434/api/tags
```

For detailed instructions, see [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md)

## Verification

### API Health Check

```bash
# Basic health
curl http://localhost:8000/health

# Response should be:
# {
#   "status": "healthy",
#   "app": "Empower AI OCR API",
#   "version": "1.0.0",
#   "environment": "development"
# }
```

### Test OCR Processing

```bash
# First, create a test API key in the database or get admin key from .env
API_KEY="your-api-key"

# Test OCR endpoint (requires an actual image file)
curl -X POST "http://localhost:8000/api/v1/ocr/process" \
  -H "X-API-Key: $API_KEY" \
  -F "file=@test_document.jpg" \
  -F "document_type_code=INVOICE"
```

### Database Connection

```bash
# Check database connection
python -c "from app.core.database import sync_engine; print(sync_engine.execute('SELECT 1'))"
```

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### PostgreSQL Connection Error

```bash
# Check if PostgreSQL is running
ps aux | grep postgres

# Check PostgreSQL logs
tail -f /var/log/postgresql/postgresql.log

# Verify connection string
psql postgresql://ocr_user:ocr_password@localhost:5432/ocr_db
```

#### Ollama Not Responding

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
killall ollama
ollama serve
```

#### Redis Connection Error

```bash
# Check Redis is running
redis-cli ping

# Should respond: PONG
```

#### Import Errors

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Getting Help

- Check logs: `tail -f logs/app.log`
- API documentation: http://localhost:8000/docs
- GitHub issues: https://github.com/empowerai/ocr-api/issues
- Email support: support@empowerai.com

## Next Steps

1. Read [API.md](API.md) for API usage examples
2. Explore [LLM_CONFIGURATION.md](LLM_CONFIGURATION.md) for LLM setup
3. Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
4. Create test documents and verify OCR functionality
5. Setup admin dashboard for managing tenants and API keys
