"""Sandbox UI for manual OCR API testing."""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Sandbox"])


@router.get("/sandbox", response_class=HTMLResponse, include_in_schema=False)
async def sandbox_page() -> HTMLResponse:
    """Serve a simple sandbox page for testing OCR API calls."""
    return HTMLResponse(
        """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Empower AI OCR Sandbox</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #0b1020;
      --panel: #121933;
      --panel-2: #182142;
      --text: #eef2ff;
      --muted: #a9b4d0;
      --accent: #67e8f9;
      --accent-2: #8b5cf6;
      --border: #2a3561;
      --success: #22c55e;
      --error: #ef4444;
      --warning: #f59e0b;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, Segoe UI, Arial, sans-serif;
      background: linear-gradient(180deg, #0a0f1f 0%, #111936 100%);
      color: var(--text);
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
    }

    .hero {
      margin-bottom: 20px;
      padding: 24px;
      border: 1px solid var(--border);
      border-radius: 18px;
      background: rgba(18, 25, 51, 0.9);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
    }

    h1 { margin: 0 0 8px; font-size: 28px; }
    p { color: var(--muted); margin: 0; }

    .grid {
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 20px;
      align-items: start;
    }

    .card {
      background: rgba(18, 25, 51, 0.92);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 18px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
    }

    .form-group { margin-bottom: 16px; }
    .label {
      display: block;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    input[type="text"], select, input[type="file"], textarea {
      width: 100%;
      background: var(--panel-2);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px 14px;
      outline: none;
    }

    input[type="text"]:focus, select:focus, textarea:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(103, 232, 249, 0.15);
    }

    textarea {
      min-height: 110px;
      resize: vertical;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 12px;
    }

    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .button {
      width: 100%;
      border: 0;
      border-radius: 12px;
      padding: 14px 16px;
      color: white;
      background: linear-gradient(135deg, var(--accent-2), var(--accent));
      font-weight: 700;
      cursor: pointer;
    }

    .button:disabled {
      opacity: 0.6;
      cursor: wait;
    }

    .status {
      margin-bottom: 14px;
      padding: 12px 14px;
      border-radius: 12px;
      border: 1px solid var(--border);
      background: var(--panel-2);
      color: var(--muted);
      min-height: 48px;
      white-space: pre-wrap;
    }

    .status.success { border-color: rgba(34, 197, 94, 0.5); color: #bbf7d0; }
    .status.error { border-color: rgba(239, 68, 68, 0.5); color: #fecaca; }
    .status.warning { border-color: rgba(245, 158, 11, 0.5); color: #fde68a; }

    .tabs {
      display: flex;
      gap: 8px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }

    .tab {
      border: 1px solid var(--border);
      background: var(--panel-2);
      color: var(--muted);
      border-radius: 10px;
      padding: 10px 14px;
      cursor: pointer;
      font-weight: 600;
    }

    .tab.active {
      color: var(--text);
      border-color: var(--accent);
      box-shadow: inset 0 0 0 1px rgba(103, 232, 249, 0.3);
    }

    .panel {
      display: none;
      background: #0a1022;
      border: 1px solid var(--border);
      border-radius: 16px;
      min-height: 540px;
      overflow: auto;
    }

    .panel.active { display: block; }

    .raw-json {
      margin: 0;
      padding: 18px;
      font-size: 13px;
      line-height: 1.55;
      white-space: pre-wrap;
      word-break: break-word;
      color: #dbeafe;
    }

    .tree {
      padding: 16px;
      font-size: 14px;
    }

    .tree-node {
      margin-left: 16px;
      padding-left: 14px;
      border-left: 1px dashed rgba(169, 180, 208, 0.25);
    }

    .tree-entry {
      margin: 8px 0;
      padding: 10px 12px;
      background: rgba(24, 33, 66, 0.6);
      border: 1px solid rgba(42, 53, 97, 0.8);
      border-radius: 10px;
    }

    .tree-key { color: #93c5fd; font-weight: 700; }
    .tree-value { color: #e9d5ff; }
    .tree-index { color: #fca5a5; font-weight: 700; }

    .meta {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 14px;
    }

    .meta-box {
      padding: 12px;
      border-radius: 12px;
      background: var(--panel-2);
      border: 1px solid var(--border);
    }

    .meta-label { color: var(--muted); font-size: 12px; margin-bottom: 4px; }
    .meta-value { font-size: 15px; font-weight: 700; }

    .hint {
      margin-top: 10px;
      font-size: 12px;
      color: var(--muted);
    }

    @media (max-width: 980px) {
      .grid { grid-template-columns: 1fr; }
      .meta { grid-template-columns: 1fr 1fr; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="hero">
      <h1>Empower AI OCR Sandbox</h1>
      <p>Upload a document, choose a document type, call the OCR API, and inspect both the flattened OCR output and ERP-ready nested JSON.</p>
    </div>

    <div class="grid">
      <div class="card">
        <div class="form-group">
          <label class="label" for="apiKey">API Key</label>
          <input id="apiKey" type="text" placeholder="Enter X-API-Key" />
        </div>

        <div class="form-group">
          <label class="label" for="documentType">Document Type</label>
          <select id="documentType">
            <option value="INVOICE">INVOICE</option>
            <option value="CHEQUE">CHEQUE</option>
            <option value="PAN_CARD">PAN_CARD</option>
            <option value="AADHAAR_CARD">AADHAAR_CARD</option>
          </select>
        </div>

        <div class="form-group">
          <label class="label" for="providerName">Provider</label>
          <select id="providerName">
            <option value="llama" selected>llama (Ovis/VM)</option>
            <option value="ollama">ollama (local glm-ocr flow)</option>
            <option value="sglang">sglang</option>
          </select>
        </div>

        <div class="form-group">
          <label class="label" for="deploymentMode">Deployment Mode</label>
          <select id="deploymentMode">
            <option value="vm" selected>vm (remote OpenAI endpoint)</option>
            <option value="local">local (ollama /api/generate)</option>
          </select>
        </div>

        <div class="form-group">
          <label class="label" for="vmBaseUrl">VM Base URL</label>
          <input id="vmBaseUrl" type="text" value="http://45.194.46.160:8000" placeholder="http://host:8000" />
        </div>

        <div class="form-group">
          <label class="label" for="modelName">Model</label>
          <select id="modelName">
            <option value="AIDC-AI/Ovis2.5-9B" selected>AIDC-AI/Ovis2.5-9B (default)</option>
            <option value="llama3.2-vision:11b">llama3.2-vision:11b</option>
            <option value="llama3.2:3b">llama3.2:3b</option>
            <option value="glm-ocr:latest">glm-ocr:latest</option>
          </select>
        </div>

        <div class="form-group">
          <label class="label" for="documentFile">Document</label>
          <input id="documentFile" type="file" accept=".pdf,.png,.jpg,.jpeg" />
        </div>

        <div class="form-group">
          <label class="label" for="promptOverride">Prompt Override (Optional)</label>
          <textarea id="promptOverride" placeholder="Leave empty to use app default prompt."></textarea>
        </div>

        <div class="row">
          <button id="submitBtn" class="button">Run OCR</button>
          <button id="resetBtn" class="button" type="button" style="background:linear-gradient(135deg,#334155,#475569);">Reset</button>
        </div>

        <div class="hint">
          Calls <strong>/api/v1/ocr/process</strong> with multipart form-data and sends the API key as <strong>X-API-Key</strong>.
        </div>
      </div>

      <div>
        <div id="status" class="status">Ready.</div>

        <div class="meta" id="meta" style="display:none;">
          <div class="meta-box"><div class="meta-label">Request ID</div><div class="meta-value" id="metaRequestId">-</div></div>
          <div class="meta-box"><div class="meta-label">Status</div><div class="meta-value" id="metaStatus">-</div></div>
          <div class="meta-box"><div class="meta-label">Confidence</div><div class="meta-value" id="metaConfidence">-</div></div>
          <div class="meta-box"><div class="meta-label">Processing Time</div><div class="meta-value" id="metaTime">-</div></div>
        </div>

        <div class="tabs">
          <button class="tab active" data-tab="visual">Visual JSON</button>
          <button class="tab" data-tab="raw">Raw JSON</button>
          <button class="tab" data-tab="erp">ERP Payload</button>
          <button class="tab" data-tab="modelraw">Model Raw</button>
        </div>

        <div id="visual" class="panel active"><div id="visualTree" class="tree"></div></div>
        <div id="raw" class="panel"><pre id="rawJson" class="raw-json">No response yet.</pre></div>
        <div id="erp" class="panel"><pre id="erpJson" class="raw-json">No ERP payload yet.</pre></div>
        <div id="modelraw" class="panel"><pre id="modelRawText" class="raw-json">No model output yet.</pre></div>
      </div>
    </div>
  </div>

  <script>
    const submitBtn = document.getElementById('submitBtn');
    const resetBtn = document.getElementById('resetBtn');
    const apiKeyInput = document.getElementById('apiKey');
    const documentTypeInput = document.getElementById('documentType');
    const providerNameInput = document.getElementById('providerName');
    const deploymentModeInput = document.getElementById('deploymentMode');
    const vmBaseUrlInput = document.getElementById('vmBaseUrl');
    const modelNameInput = document.getElementById('modelName');
    const documentFileInput = document.getElementById('documentFile');
    const promptOverrideInput = document.getElementById('promptOverride');
    const statusEl = document.getElementById('status');
    const visualTreeEl = document.getElementById('visualTree');
    const rawJsonEl = document.getElementById('rawJson');
    const erpJsonEl = document.getElementById('erpJson');
    const modelRawEl = document.getElementById('modelRawText');
    const metaEl = document.getElementById('meta');

    const metaRequestId = document.getElementById('metaRequestId');
    const metaStatus = document.getElementById('metaStatus');
    const metaConfidence = document.getElementById('metaConfidence');
    const metaTime = document.getElementById('metaTime');

    function setStatus(message, type = '') {
      statusEl.textContent = message;
      statusEl.className = 'status' + (type ? ' ' + type : '');
    }

    function escapeHtml(value) {
      return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    function renderTree(value, key = null) {
      if (Array.isArray(value)) {
        const items = value.map((item, index) => `
          <div class="tree-node">
            <div class="tree-entry"><span class="tree-index">[${index}]</span></div>
            ${renderTree(item)}
          </div>
        `).join('');
        return key === null
          ? items
          : `<div class="tree-entry"><span class="tree-key">${escapeHtml(key)}</span>: <span class="tree-value">[array]</span></div>${items}`;
      }

      if (value && typeof value === 'object') {
        const entries = Object.entries(value).map(([childKey, childValue]) => `
          <div class="tree-node">${renderTree(childValue, childKey)}</div>
        `).join('');
        return key === null
          ? entries
          : `<div class="tree-entry"><span class="tree-key">${escapeHtml(key)}</span>: <span class="tree-value">{object}</span></div>${entries}`;
      }

      const printable = value === null ? 'null' : escapeHtml(value);
      return `<div class="tree-entry"><span class="tree-key">${escapeHtml(key ?? 'value')}</span>: <span class="tree-value">${printable}</span></div>`;
    }

    function activateTab(tabName) {
      document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === tabName);
      });
      document.querySelectorAll('.panel').forEach(panel => {
        panel.classList.toggle('active', panel.id === tabName);
      });
    }

    document.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => activateTab(tab.dataset.tab));
    });

    resetBtn.addEventListener('click', () => {
      apiKeyInput.value = '';
      documentTypeInput.value = 'INVOICE';
      providerNameInput.value = 'llama';
      deploymentModeInput.value = 'vm';
      vmBaseUrlInput.value = 'http://45.194.46.160:8000';
      modelNameInput.value = 'AIDC-AI/Ovis2.5-9B';
      documentFileInput.value = '';
      promptOverrideInput.value = '';
      visualTreeEl.innerHTML = '';
      rawJsonEl.textContent = 'No response yet.';
      erpJsonEl.textContent = 'No ERP payload yet.';
      modelRawEl.textContent = 'No model output yet.';
      metaEl.style.display = 'none';
      setStatus('Ready.');
      activateTab('visual');
    });

    submitBtn.addEventListener('click', async () => {
      const apiKey = apiKeyInput.value.trim();
      const file = documentFileInput.files[0];
      const documentType = documentTypeInput.value;
      const providerName = providerNameInput.value;
      const deploymentMode = deploymentModeInput.value;
      const vmBaseUrl = vmBaseUrlInput.value.trim();
      const modelName = modelNameInput.value;
      const promptOverride = promptOverrideInput.value.trim();

      if (!apiKey) {
        setStatus('API key is required.', 'warning');
        return;
      }

      if (!file) {
        setStatus('Please select a document.', 'warning');
        return;
      }

      const formData = new FormData();
      formData.append('file', file);
      formData.append('document_type_code', documentType);
      formData.append('provider_name', providerName);
      formData.append('deployment_mode', deploymentMode);
      if (vmBaseUrl) {
        formData.append('vm_base_url', vmBaseUrl);
      }
      formData.append('model_name', modelName);
      if (promptOverride) {
        formData.append('prompt_override', promptOverride);
      }

      submitBtn.disabled = true;
      setStatus(`Uploading document and waiting for OCR response...\nProvider: ${providerName}\nDeployment: ${deploymentMode}\nVM URL: ${vmBaseUrl || '(default)'}\nModel: ${modelName}`, 'warning');

      try {
        const response = await fetch('/api/v1/ocr/process', {
          method: 'POST',
          headers: {
            'X-API-Key': apiKey,
          },
          body: formData,
        });

        const text = await response.text();
        let data;
        try {
          data = JSON.parse(text);
        } catch {
          throw new Error(text || 'Invalid non-JSON response from server.');
        }

        rawJsonEl.textContent = JSON.stringify(data, null, 2);
        erpJsonEl.textContent = JSON.stringify(data.erp_payload ?? {}, null, 2);
        modelRawEl.textContent = data.raw_model_output ?? '(no raw_model_output in response)';
        visualTreeEl.innerHTML = renderTree(data);
        metaEl.style.display = 'grid';
        metaRequestId.textContent = data.request_id || '-';
        metaStatus.textContent = data.status || '-';
        metaConfidence.textContent = data.confidence_level || '-';
        metaTime.textContent = typeof data.processing_time_ms === 'number' ? `${data.processing_time_ms} ms` : '-';

        if (!response.ok) {
          setStatus(`Request failed (${response.status}). See JSON output for details.`, 'error');
        } else {
          setStatus('OCR completed successfully.', 'success');
        }
      } catch (error) {
        rawJsonEl.textContent = String(error);
      erpJsonEl.textContent = 'No ERP payload available.';
      modelRawEl.textContent = 'No model output available.';
      visualTreeEl.innerHTML = `<div class="tree-entry"><span class="tree-key">error</span>: <span class="tree-value">${escapeHtml(error.message || error)}</span></div>`;
        metaEl.style.display = 'none';
        setStatus(`Request failed: ${error.message || error}`, 'error');
      } finally {
        submitBtn.disabled = false;
      }
    });
  </script>
</body>
</html>
        """
    )
