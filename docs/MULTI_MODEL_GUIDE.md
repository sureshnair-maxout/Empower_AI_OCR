# Multi-Model OCR Framework - Quick Reference

## Overview
The application now supports multiple vision models with easy switching via configuration.

## Available Providers

### 1. **GLM-OCR** (Provider: `ollama`)
- **Model**: `glm-ocr:latest` (1.1B parameters, F16 quantization)
- **Best for**: Fast OCR, Chinese documents, table extraction
- **Strategy**: Dual-prompt (Text Recognition + Table Recognition) with post-processing
- **Speed**: ~15-25 seconds per invoice
- **Model size**: ~2.2GB

### 2. **Llama 3.2 Vision** (Provider: `llama`)
- **Model**: `llama3.2-vision:11b` (11B parameters)
- **Best for**: Complex reasoning, structured extraction, instruction following
- **Strategy**: Single structured prompt with JSON output
- **Speed**: ~30-60 seconds per invoice
- **Model size**: ~7GB

## Configuration

### Method 1: Environment Variables (Docker)
Edit `docker/docker-compose.yml`:

```yaml
environment:
  LLM_PROVIDER: llama  # or "ollama" for GLM-OCR
  LLAMA_MODEL_NAME: llama3.2-vision:11b
  GLM_OCR_MODEL_NAME: glm-ocr:latest
  LLM_TIMEOUT_SECONDS: 180
```

### Method 2: .env File (Local)
Create/edit `.env` in project root:

```env
LLM_PROVIDER=llama
LLAMA_MODEL_NAME=llama3.2-vision:11b
GLM_OCR_MODEL_NAME=glm-ocr:latest
OLLAMA_BASE_URL=http://localhost:11434
LLM_TIMEOUT_SECONDS=180
```

### Method 3: Runtime (API Parameter)
Future enhancement: Pass `provider` parameter in API request

## Switching Models

### Switch to Llama 3.2 Vision:
```bash
# Update docker-compose.yml: LLM_PROVIDER=llama
docker-compose -f docker/docker-compose.yml up -d api
```

### Switch to GLM-OCR:
```bash
# Update docker-compose.yml: LLM_PROVIDER=ollama
docker-compose -f docker/docker-compose.yml up -d api
```

### No rebuild required - just restart container!

## Model Installation

### Install Llama 3.2 Vision (if not already):
```bash
ollama pull llama3.2-vision:11b
```

### Install GLM-OCR (if not already):
```bash
ollama pull glm-ocr:latest
```

### Verify installation:
```bash
ollama list
```

## Testing

### Test with invoice document:
```bash
curl -X POST "http://localhost:8000/api/v1/ocr/process" \
  -H "X-API-Key: test-key" \
  -F "document_type_code=INVOICE" \
  -F "file=@/path/to/invoice.pdf"
```

### Check which model is active:
```bash
docker logs ocr_api 2>&1 | grep "model"
```

## Performance Comparison

| Metric | GLM-OCR | Llama 3.2 Vision |
|--------|---------|------------------|
| Speed | ⚡⚡⚡ Fast | ⚡⚡ Moderate |
| Accuracy | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Excellent |
| Memory | 3GB VRAM | 8GB VRAM |
| Structured Output | Post-processing | Native JSON |
| Complex Reasoning | Limited | Strong |

## Recommended Use Cases

### Use GLM-OCR when:
- Processing high volumes (>100 docs/hour)
- Simple field extraction (invoice number, date, total)
- Limited GPU memory (<6GB)
- Chinese/multilingual documents

### Use Llama 3.2 Vision when:
- Complex document layout
- Need high accuracy (>95%)
- Handling edge cases (unusual formats)
- Extracting nested/conditional fields

## Adding New Models

1. Create provider in `app/llm/providers/your_model.py`
2. Implement `LLMProvider` interface
3. Register in `app/llm/providers/__init__.py`
4. Add config settings in `app/core/config.py`
5. Test and document

## Troubleshooting

### Model not found error:
```bash
# Pull the model first
ollama pull <model-name>

# Verify it's available
ollama list
```

### Timeout errors with Llama:
```yaml
# Increase timeout in docker-compose.yml
LLM_TIMEOUT_SECONDS: 300  # 5 minutes
```

### Memory issues:
- Use smaller Llama variant: `llama3.2-vision:3b`
- Or stick with GLM-OCR for limited hardware

## Future Enhancements

- [ ] Runtime model switching via API parameter
- [ ] Model performance metrics dashboard
- [ ] Automatic model selection based on document complexity
- [ ] Model response caching
- [ ] Parallel processing with multiple models
- [ ] Fine-tuned models for specific invoice formats
