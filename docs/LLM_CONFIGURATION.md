# LLM Provider Configuration Guide

## Overview

The Empower AI OCR API abstracts the LLM inference layer, making it easy to switch between different providers without code changes. This document explains how to configure and switch between providers.

## Supported Providers

### 1. Ollama (Default)

**Ollama** is a lightweight LLM serving framework that runs models locally.

#### Prerequisites
- Install Ollama from https://ollama.ai
- Download GLM-OCR model: `ollama pull glm-ocr`
- Ollama running on port 11434

#### Configuration

Environment variables:
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OCR_MODEL_NAME=glm-ocr
OCR_MODEL_VERSION=latest
LLM_TIMEOUT_SECONDS=120
LLM_MAX_RETRIES=3
```

#### Features
- ✅ Free and open-source
- ✅ Local execution (no data leaves your infrastructure)
- ✅ Low latency
- ✅ India data localization compliant
- ✅ Supports multiple model formats

#### Setup Commands
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve

# (In another terminal) Pull GLM-OCR model
ollama pull glm-ocr

# Test the setup
curl http://localhost:11434/api/tags
```

### 2. SGLang

**SGLang** is a high-performance framework for serving language models with advanced features.

#### Prerequisites
- Install SGLang: `pip install sglang[all]`
- Download model compatible with SGLang
- SGLang server running on port 30000

#### Configuration

Environment variables:
```env
LLM_PROVIDER=sglang
SGLANG_BASE_URL=http://localhost:30000
OCR_MODEL_NAME=glm-ocr
LLM_TIMEOUT_SECONDS=120
LLM_MAX_RETRIES=3
```

#### Setup Commands
```bash
# Install SGLang
pip install sglang[all]

# Start SGLang server with GLM-OCR model
python -m sglang.launch_server --model-path glm-ocr --port 30000

# Test the setup
curl http://localhost:30000/health
```

#### Features
- ✅ High throughput
- ✅ Advanced optimization
- ✅ Multi-GPU support
- ✅ Efficient batching

### 3. Local Custom Provider (Template)

Create a custom provider for other LLM frameworks:

```python
# app/llm/providers/custom.py
from app.llm.base import LLMProvider, LLMProviderFactory, OCRRequest, OCRResponse

class CustomProvider(LLMProvider):
    async def process_ocr(self, request: OCRRequest) -> OCRResponse:
        # Implement your custom logic
        pass

    async def health_check(self) -> bool:
        # Check provider health
        pass

    async def get_model_info(self) -> dict:
        # Return model information
        pass

# Register the provider
LLMProviderFactory.register("custom", CustomProvider)
```

Then set: `LLM_PROVIDER=custom`

## Switching Providers

### Step 1: Update Environment Variables

Edit `.env`:
```env
# Change provider
LLM_PROVIDER=sglang
# Update endpoint
SGLANG_BASE_URL=http://your-sglang-server:30000
```

### Step 2: Restart the Application

```bash
# Docker
docker-compose restart api

# Or manually
uvicorn app.main:app --reload
```

### Step 3: Verify Health

```bash
curl -H "X-API-Key: your-key" http://localhost:8000/api/v1/ocr/health
```

## Model Versioning

### Managing Model Versions

```env
OCR_MODEL_NAME=glm-ocr
OCR_MODEL_VERSION=1.0
```

### Fallback Strategy

Implement fallback providers:

```python
# app/llm/manager.py
providers = [
    LLMProviderFactory.create("ollama"),
    LLMProviderFactory.create("sglang"),
]

async def get_available_provider():
    for provider in providers:
        if await provider.health_check():
            return provider
    raise ProviderNotAvailableError("No providers available")
```

## Performance Tuning

### Ollama Optimization

```bash
# Enable GPU acceleration (if available)
OLLAMA_GPU=1 ollama serve

# Set number of processing threads
OLLAMA_NUM_THREAD=16 ollama serve

# Control context window
OLLAMA_MAX_CONTEXT=4096 ollama serve
```

### SGLang Optimization

```bash
# Multi-GPU setup
python -m sglang.launch_server \
  --model-path glm-ocr \
  --port 30000 \
  --tensor-parallel 2 \
  --batch-size 32
```

### API Configuration

```env
# Timeout for LLM inference
LLM_TIMEOUT_SECONDS=120

# Retry configuration
LLM_MAX_RETRIES=3

# Connection pooling
DATABASE_POOL_SIZE=10
```

## Monitoring & Debugging

### Check Provider Health

```bash
curl http://localhost:8000/api/v1/ocr/health
```

### View Logs

```bash
# Docker logs
docker-compose logs -f api

# Application logs
tail -f logs/app.log
```

### Metrics

Access Jaeger UI for tracing:
- http://localhost:16686

### Common Issues

| Issue | Solution |
|-------|----------|
| Connection refused | Ensure provider server is running |
| Timeout errors | Increase LLM_TIMEOUT_SECONDS |
| High latency | Check provider resources, increase OLLAMA_NUM_THREAD |
| Low confidence scores | Verify model is downloaded correctly, check input quality |

## Advanced Configuration

### Custom Model Parameters

Pass custom parameters to provider:

```python
# app/llm/manager.py
provider = LLMProviderFactory.create(
    "ollama",
    temperature=0.1,  # Lower for consistency
    top_p=0.9,
    top_k=40,
)
```

### Batch Processing

For high-volume processing:

```python
# Use async processing
import asyncio

tasks = [
    ocr_service.process_document(path, doc_type, org_id)
    for path in document_paths
]
results = await asyncio.gather(*tasks)
```

## Cost Analysis

| Provider | Cost | Maintenance | Scalability |
|----------|------|-------------|-------------|
| **Ollama** | Free | Self-hosted | Limited by hardware |
| **SGLang** | Free | Self-hosted | Better with multi-GPU |
| **Cloud API** | Pay-per-use | Managed | Unlimited |

## Migration Guide

### From Ollama to SGLang

1. Install SGLang with same model
2. Update `.env`: LLM_PROVIDER=sglang
3. Test with sample documents
4. Monitor performance and adjust threading
5. Gradually migrate production load

### Rollback

Keep previous provider configuration in git:
```bash
git checkout previous-branch -- .env
docker-compose restart api
```

## Support & Documentation

- **Ollama**: https://ollama.ai/library
- **SGLang**: https://sglang.run/docs
- **OpenAI API**: https://platform.openai.com/docs

For help: support@empowerai.com
