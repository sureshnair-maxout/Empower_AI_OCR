# Empower AI OCR API

Last updated: 2026-03-17

This document tracks the API surface currently implemented in this repository.

## Base URL

- Local: `http://localhost:8000`
- API prefix: `/api/v1`

## Authentication

Protected endpoints require API key header:

```bash
X-API-Key: <your-api-key>
```

## Implemented Endpoints

### 1) Service Health (no API key)

#### GET /health

Basic service health probe.

Response example:

```json
{
  "status": "healthy",
  "app": "Empower AI OCR API",
  "version": "1.0.0",
  "environment": "development"
}
```

---

### 2) OCR Process (API key required)

#### POST /api/v1/ocr/process

Processes an uploaded document and returns flattened OCR fields plus optional nested ERP payload.

Content type: `multipart/form-data`

Form fields:

- `file` (required): `.jpg`, `.jpeg`, `.png`, `.pdf`
- `document_type_code` (required): e.g., `INVOICE`, `CHEQUE`, `PO`, `LR`, `PAN_CARD`, `AADHAAR_CARD`
- `provider_name` (optional): `llama` | `ollama` | `sglang`
- `deployment_mode` (optional): `vm` | `local`
- `vm_base_url` (optional): e.g., `http://64.247.196.84:8000`
- `model_name` (optional): model override (e.g., `AIDC-AI/Ovis2.5-9B`)
- `prompt_override` (optional): prompt override text

Request example:

```bash
curl -X POST "http://localhost:8000/api/v1/ocr/process" \
  -H "X-API-Key: your-api-key" \
  -F "file=@D:/Documents/0124-1.jpg" \
  -F "document_type_code=INVOICE" \
  -F "provider_name=llama" \
  -F "deployment_mode=vm" \
  -F "vm_base_url=http://64.247.196.84:8000" \
  -F "model_name=AIDC-AI/Ovis2.5-9B"
```

Response example:

```json
{
  "request_id": "6f7b389e-e98f-4d4d-9d8d-9d2de4c6f55d",
  "document_type": "INVOICE",
  "status": "success",
  "ocr_results": {
    "invoice_details.invoice_no": {
      "value": "25-26/0077",
      "confidence": 0.98,
      "data_type": "string",
      "required": false,
      "raw_text": "25-26/0077"
    },
    "invoice_details.invoice_type": {
      "value": "Tax Invoice",
      "confidence": 0.93,
      "data_type": "string",
      "required": false,
      "raw_text": "Tax Invoice"
    }
  },
  "confidence_level": "HIGH",
  "processing_time_ms": 4120,
  "warnings": [],
  "errors": [],
  "model_version": "AIDC-AI/Ovis2.5-9B",
  "erp_payload": {
    "vendor_details": {},
    "invoice_details": {},
    "transport_details": {},
    "bank_details": {},
    "items": []
  },
  "raw_model_output": "{ ... raw model text ... }"
}
```

Field notes:

- `ocr_results` is a flattened key-value map where each value has `value`, `confidence`, `data_type`, `required`, `raw_text`.
- `erp_payload` is nested JSON from model output when parse succeeds.
- `raw_model_output` is the full model text response before parsing.
- `confidence_level` is computed aggregate: `HIGH`, `MEDIUM`, `LOW`, `VERY_LOW`.

Status codes:

- `200`: OCR request processed
- `401`: Missing/invalid API key
- `500`: Server-side OCR failure

---

### 3) OCR Provider Health (API key required)

#### GET /api/v1/ocr/health

Checks configured OCR provider/model health.

Response example:

```json
{
  "status": "healthy",
  "provider": "ollama",
  "model": {
    "name": "AIDC-AI/Ovis2.5-9B",
    "status": "available"
  }
}
```

---

### 4) Sandbox UI (no API key to open page)

#### GET /sandbox

Manual test page for `/api/v1/ocr/process` with:

- Provider/model/deployment selectors
- VM base URL input
- Optional prompt override
- Tabs for visual JSON, raw JSON, ERP payload, and raw model output

Note: actual OCR submit from sandbox still requires a valid API key.

## Non-Exposed / Not Yet Active Routes

The following files exist but are not currently mounted in `app/main.py`:

- `app/api/v1/admin.py`
- `app/api/v1/tenancy.py`

Do not rely on those routes until they are included in the main app router.

## Error Handling Guidance

- Treat `500` body `detail` as actionable runtime failure detail.
- Implement retries with exponential backoff for transient network/model errors.
- Validate low-confidence fields (`LOW`/`VERY_LOW`) in downstream ERP workflows.

## Documentation Maintenance

This file should be updated whenever any of these change:

- API route path/method/signature
- Request form fields
- Response schema fields
- Authentication requirements
- Mounted routers in `app/main.py`
