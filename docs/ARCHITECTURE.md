# Architecture & Design Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Client Applications                         │
│                 (ERP Systems, Frontend, etc.)                    │
└──────────────────────┬──────────────────────────────────────────┘
                       │
          ┌────────────▼────────────┐
          │   API Gateway / NGINX   │
          │  (Rate Limiting, TLS)   │
          └────────────┬────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                     FastAPI Gateway                              │
│          (Request Validation, Authentication)                    │
└───────────┬────────────────┬────────────────┬────────────────────┘
            │                │                │
      ┌─────▼──────┐   ┌─────▼──────┐   ┌────▼──────┐
      │  OCR       │   │ Tenancy    │   │  Billing  │
      │  Service   │   │  Service   │   │  Service  │
      └─────┬──────┘   └─────┬──────┘   └────┬──────┘
            │                │                │
      ┌─────▼──────────────────────────────────┴──────┐
      │   Core Business Logic Layer                   │
      │  (Validation, Processing, Orchestration)      │
      └─────┬──────────────────────────────────┬──────┘
            │                                  │
      ┌─────▼──────┐    ┌──────────────────┐   │
      │  LLM       │    │  Data Access      │   │
      │  Abstraction    │  Layer (SQLAlchemy)  │
      └─────┬──────┘    │  (ORM)            │   │
            │           └──────────┬────────┘   │
            │                      │            │
      ┌─────▼──────┐         ┌─────▼─────┐  ┌─▼──────────┐
      │ Ollama     │         │PostgreSQL │  │   Redis    │
      │ GLM-OCR    │         │ Database  │  │   Cache    │
      │ SGLang     │         │           │  │            │
      └────────────┘         └───────────┘  └────────────┘

         Observability Layer
         ┌──────────────────────────────────┐
         │  OpenTelemetry / Jaeger Tracing  │
         │  Structured Logging              │
         │  Metrics Collection              │
         └──────────────────────────────────┘
```

## Component Architecture

### 1. API Layer (`app/api/`)
- **Purpose**: HTTP request handling and routing
- **Endpoints**:
  - `/api/v1/ocr/process` - Document OCR processing
  - `/api/v1/ocr/health` - Health check
  - `/api/v1/tenants/*` - Tenant management
  - `/api/v1/admin/*` - Admin operations
  - `/api/v1/billing/*` - Billing operations
- **Responsibilities**:
  - Request validation
  - Authentication & authorization
  - Response formatting
  - Error handling

### 2. Service Layer (`app/services/`)
- **Purpose**: Business logic implementation
- **Services**:
  - `OCRService` - Document OCR orchestration
  - `BillingService` - Usage tracking and billing
  - `TenantService` - Tenant management
  - `DocumentTypeService` - Schema management
- **Responsibilities**:
  - Business logic
  - Service coordination
  - Data transformation
  - Exception handling

### 3. LLM Abstraction Layer (`app/llm/`)
- **Purpose**: Abstract LLM provider implementation
- **Design Pattern**: Factory + Strategy
- **Providers**:
  - `OllamaProvider` - Local Ollama with GLM-OCR
  - `SGLangProvider` - SGLang framework
  - `CustomProvider` - Template for custom implementations
- **Benefits**:
  - Easy provider switching
  - No code changes for different models
  - Pluggable architecture

### 4. Data Access Layer (`app/models/`, `app/core/database.py`)
- **Purpose**: Database interaction and persistence
- **Technology**: SQLAlchemy ORM with async support
- **Models**:
  - `Organization` - Tenant data
  - `APIKey` - Authentication credentials
  - `Document` - Document metadata
  - `OCRResult` - Processing results
  - `BillingRecord` - Usage & billing data
  - `AuditLog` - Compliance logging
- **Features**:
  - Automatic timestamp management
  - Soft deletes support
  - Audit trail
  - Multi-tenancy enforcement

### 5. Authentication & Authorization (`app/auth/`)
- **Purpose**: Security and access control
- **Methods**:
  - API Key authentication
  - JWT token-based access
  - Role-based access control (RBAC)
- **Features**:
  - Password hashing (bcrypt)
  - Token generation and validation
  - API key management
  - Admin access control

### 6. Multi-Tenancy (`app/tenancy/`)
- **Purpose**: Tenant isolation and context management
- **Implementation**:
  - Context variables for org_id tracking
  - Query-level filtering
  - Data isolation
- **Benefits**:
  - Automatic data segregation
  - Tenant-specific configuration
  - Per-tenant rate limiting

### 7. Billing Module (`app/billing/`)
- **Purpose**: Usage tracking and billing
- **Features**:
  - Real-time usage recording
  - Monthly aggregation
  - Multiple billing models
  - Invoice generation (future)

### 8. Observability (`app/observability/`)
- **Purpose**: System monitoring and troubleshooting
- **Components**:
  - OpenTelemetry instrumentation
  - Jaeger tracing
  - Structured logging
  - Metrics collection

## Data Flow

### OCR Processing Flow

```
Client Request
    ↓
API Validation (FastAPI)
    ↓
Authentication (API Key)
    ↓
Tenant Context Setup
    ↓
Document Validation
    ├─ Format check
    ├─ Size validation
    └─ Type detection
    ↓
OCR Service Processing
    ├─ Load document
    ├─ Generate prompt (with schema)
    ├─ Call LLM (via abstraction)
    ├─ Parse response
    └─ Calculate confidence
    ↓
Result Validation
    ├─ Data type checking
    ├─ Field validation
    └─ Confidence thresholds
    ↓
Billing Recording (if enabled)
    ↓
ERP Payload Generation
    ↓
Response to Client
```

## Multi-Tenancy Architecture

### Tenant Isolation Levels

1. **Authentication Level**
   - API keys tied to organizations
   - JWT tokens include org_id

2. **Query Level**
   - All queries filtered by org_id
   - SQLAlchemy filters automatically applied

3. **Application Level**
   - Context variables track current org
   - Services enforce org_id checks

4. **Data Level**
   - Database constraints on org_id
   - Separate indexes per tenant

### Schema for Multi-Tenancy

```
Organization
├── APIKey (1-to-Many)
├── Document (1-to-Many)
├── DocumentType (1-to-Many)
├── BillingRecord (1-to-Many)
└── AuditLog (1-to-Many)
```

## Deployment Modes

### Tenant Mode (SaaS)
- Multiple organizations support
- Billing enabled
- Multi-tenancy enforced
- Separate API keys per org
- Usage tracking

Configuration:
```env
DEPLOYMENT_MODE=tenant
ENABLE_BILLING=true
```

### Owner Mode (Single-Tenant)
- Single organization
- Billing disabled
- Simplified configuration
- No tenant routing

Configuration:
```env
DEPLOYMENT_MODE=owner
ENABLE_BILLING=false
```

## Security Architecture

### Authentication Chain

```
Request
    ↓
Extract API Key from Header
    ↓
Validate API Key exists and is active
    ↓
Retrieve org_id from key metadata
    ↓
Set tenant context
    ↓
Proceed with request
```

### PII Protection

1. **Detection**
   - Regex patterns for Aadhaar, PAN, phone, email
   - Automatic field masking

2. **Storage**
   - Field-level encryption options
   - Automatic masking in logs

3. **Transmission**
   - HTTPS only
   - API response masking

4. **Retention**
   - Auto-delete after processing
   - Optional archival

## Error Handling Strategy

```
Error Occurrence
    ↓
Classification
├─ Client Error (4xx) → Return user-friendly message
├─ Server Error (5xx) → Log details, return generic message
└─ Service Error → Implement retry logic
    ↓
Logging
├─ Structured format
├─ Request ID correlation
├─ PII redaction
└─ Trace context
    ↓
Metrics
├─ Error rate tracking
├─ Alert triggering
└─ Dashboard visibility
```

## Scaling Considerations

### Horizontal Scaling
- Stateless API design
- Redis for session management
- Database connection pooling
- Load balancer for traffic distribution

### Vertical Scaling
- Async request handling
- Background job processing (future)
- Connection optimization
- Memory efficiency

### Cost Optimization
- Document auto-deletion (no storage)
- JSON archive optional
- Configurable retention
- Usage-based billing

## Future Enhancements

1. **Advanced ML**
   - Model versioning and A/B testing
   - Custom model training
   - Confidence score calibration

2. **Integrations**
   - Webhook support
   - OAuth 2.0
   - Third-party service connectors

3. **Performance**
   - Async document processing
   - Batch processing API
   - Document caching

4. **Analytics**
   - Advanced billing dashboard
   - Usage analytics
   - Performance insights

5. **Compliance**
   - GDPR compliance features
   - Advanced audit trails
   - Data residency options
