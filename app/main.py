"""Main FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from app.core.config import settings
from app.observability.telemetry import setup_otel

# Import routers
from app.api.v1 import admin
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


@app.get("/", response_class=HTMLResponse, tags=["Landing"])
async def landing_page() -> HTMLResponse:
    """Simple landing page with links to primary app entry points."""
    return HTMLResponse(
    """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Empower AI OCR</title>
    <style>
        body { font-family: Inter, Segoe UI, Arial, sans-serif; background:#0f172a; color:#e2e8f0; margin:0; }
        .wrap { max-width: 900px; margin: 48px auto; padding: 24px; }
        .card { background:#111827; border:1px solid #1f2937; border-radius:16px; padding:24px; }
        h1 { margin-top:0; }
        ul { line-height: 1.9; }
        a { color:#67e8f9; text-decoration:none; }
        a:hover { text-decoration:underline; }
        .muted { color:#94a3b8; }
    </style>
</head>
<body>
    <div class="wrap">
        <div class="card">
            <h1>Empower AI OCR</h1>
            <p class="muted">Choose an entry point below.</p>
            <ul>
                <li><a href="/sandbox">Sandbox UI</a></li>
                <li><a href="/admin-ui">Admin UI</a></li>
                <li><a href="/docs">API Docs (Swagger)</a></li>
                <li><a href="/redoc">API Docs (ReDoc)</a></li>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/api/v1/admin/dashboard">Admin Dashboard API</a> <span class="muted">(requires X-API-Key + X-Admin-Key)</span></li>
            </ul>
        </div>
    </div>
</body>
</html>
                """
        )


@app.get("/admin-ui", response_class=HTMLResponse, tags=["Admin"])
async def admin_ui_page() -> HTMLResponse:
        """Minimal admin UI for calling admin endpoints."""
        return HTMLResponse(
                """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Empower AI OCR - Admin UI</title>
    <style>
        body { font-family: Inter, Segoe UI, Arial, sans-serif; background:#0f172a; color:#e2e8f0; margin:0; }
        .wrap { max-width: 1100px; margin: 24px auto; padding: 20px; }
        .card { background:#111827; border:1px solid #1f2937; border-radius:12px; padding:16px; margin-bottom:16px; }
        .row { display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap:10px; margin-bottom:10px; }
        .row-2 { display:grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap:10px; margin-bottom:10px; }
        input, textarea { width:100%; background:#0b1220; color:#e2e8f0; border:1px solid #334155; border-radius:8px; padding:10px; }
        textarea { min-height: 140px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
        button { background:#22d3ee; color:#082f49; border:0; border-radius:8px; padding:10px 14px; font-weight:700; cursor:pointer; margin-right:8px; }
        h1, h2 { margin-top:0; }
        pre { margin:0; white-space:pre-wrap; word-break:break-word; background:#020617; border:1px solid #1e293b; border-radius:8px; padding:12px; }
        .muted { color:#94a3b8; font-size: 13px; }
        .actions { margin: 8px 0 12px; }
    </style>
</head>
<body>
    <div class="wrap">
        <div class="card">
            <h1>Admin UI</h1>
            <div class="muted">Uses admin APIs under /api/v1/admin. Provide both keys below.</div>
            <div class="row">
                <input id="apiKey" type="text" placeholder="X-API-Key" />
                <input id="adminKey" type="text" placeholder="X-Admin-Key" />
                <input id="tenantId" type="text" placeholder="tenant_id (for billing/list/create)" />
            </div>
        </div>

        <div class="card">
            <h2>Dashboard</h2>
            <div class="actions"><button id="btnDashboard">Load Dashboard</button></div>
            <pre id="outDashboard">No response yet.</pre>
        </div>

        <div class="card">
            <h2>Billing</h2>
            <div class="actions"><button id="btnBilling">Load Billing</button></div>
            <pre id="outBilling">No response yet.</pre>
        </div>

        <div class="card">
            <h2>Document Types</h2>
            <div class="actions">
                <button id="btnListDocTypes">List Document Types</button>
            </div>
            <div class="row-2">
                <input id="docTypeCode" type="text" placeholder="code (e.g. INVOICE)" />
                <input id="docTypeName" type="text" placeholder="name" />
            </div>
            <div class="row-2">
                <input id="docTypeDesc" type="text" placeholder="description" />
                <input id="docTypeActive" type="text" value="true" placeholder="is_active: true/false" />
            </div>
            <textarea id="docTypeSchema" placeholder='schema_config JSON, e.g. {"fields":["field1","field2"]}'>{"fields":[]}</textarea>
            <div class="actions"><button id="btnCreateDocType">Create Document Type</button></div>
            <pre id="outDocTypes">No response yet.</pre>
        </div>
    </div>

    <script>
        const apiKeyEl = document.getElementById('apiKey');
        const adminKeyEl = document.getElementById('adminKey');
        const tenantIdEl = document.getElementById('tenantId');

        const outDashboard = document.getElementById('outDashboard');
        const outBilling = document.getElementById('outBilling');
        const outDocTypes = document.getElementById('outDocTypes');

        const docTypeCodeEl = document.getElementById('docTypeCode');
        const docTypeNameEl = document.getElementById('docTypeName');
        const docTypeDescEl = document.getElementById('docTypeDesc');
        const docTypeActiveEl = document.getElementById('docTypeActive');
        const docTypeSchemaEl = document.getElementById('docTypeSchema');

        function getHeaders() {
            return {
                'X-API-Key': apiKeyEl.value.trim(),
                'X-Admin-Key': adminKeyEl.value.trim(),
                'Content-Type': 'application/json',
            };
        }

        async function callApi(url, opts = {}) {
            const response = await fetch(url, opts);
            const text = await response.text();
            let parsed;
            try { parsed = JSON.parse(text); } catch { parsed = { raw: text }; }
            return { ok: response.ok, status: response.status, data: parsed };
        }

        function setOutput(el, payload) {
            el.textContent = JSON.stringify(payload, null, 2);
        }

        document.getElementById('btnDashboard').addEventListener('click', async () => {
            const result = await callApi('/api/v1/admin/dashboard', {
                method: 'GET',
                headers: {
                    'X-API-Key': apiKeyEl.value.trim(),
                    'X-Admin-Key': adminKeyEl.value.trim(),
                },
            });
            setOutput(outDashboard, result);
        });

        document.getElementById('btnBilling').addEventListener('click', async () => {
            const tenantId = tenantIdEl.value.trim();
            if (!tenantId) {
                setOutput(outBilling, { error: 'tenant_id is required' });
                return;
            }
            const result = await callApi(`/api/v1/admin/billing?tenant_id=${encodeURIComponent(tenantId)}`, {
                method: 'GET',
                headers: {
                    'X-API-Key': apiKeyEl.value.trim(),
                    'X-Admin-Key': adminKeyEl.value.trim(),
                },
            });
            setOutput(outBilling, result);
        });

        document.getElementById('btnListDocTypes').addEventListener('click', async () => {
            const tenantId = tenantIdEl.value.trim();
            const url = tenantId
                ? `/api/v1/admin/document-types?tenant_id=${encodeURIComponent(tenantId)}`
                : '/api/v1/admin/document-types';
            const result = await callApi(url, {
                method: 'GET',
                headers: {
                    'X-API-Key': apiKeyEl.value.trim(),
                    'X-Admin-Key': adminKeyEl.value.trim(),
                },
            });
            setOutput(outDocTypes, result);
        });

        document.getElementById('btnCreateDocType').addEventListener('click', async () => {
            const tenantId = tenantIdEl.value.trim();
            let schema;
            try {
                schema = JSON.parse(docTypeSchemaEl.value || '{}');
            } catch {
                setOutput(outDocTypes, { error: 'schema_config must be valid JSON' });
                return;
            }

            const payload = {
                tenant_id: tenantId || null,
                code: docTypeCodeEl.value.trim(),
                name: docTypeNameEl.value.trim(),
                description: docTypeDescEl.value.trim() || null,
                schema_config: schema,
                is_active: (docTypeActiveEl.value || 'true').toLowerCase() === 'true',
            };

            const result = await callApi('/api/v1/admin/document-types', {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify(payload),
            });
            setOutput(outDocTypes, result);
        });
    </script>
</body>
</html>
                """
        )


# API v1 routes
# Health router intentionally not exposed separately (root /health exists)
app.include_router(ocr.router, prefix=settings.api_prefix, tags=["OCR"])
app.include_router(sandbox_router)
# app.include_router(tenancy.router, prefix=settings.api_prefix, tags=["Tenancy"])
app.include_router(admin.router, prefix=settings.api_prefix, tags=["Admin"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        access_log=True,
    )
