"""OCR API Provider initialization."""

# Import and register all LLM providers
from app.llm.providers.ollama import OllamaProvider  # noqa
from app.llm.providers.llama import LlamaVisionProvider  # noqa
from app.llm.providers.sglang import SGLangProvider  # noqa

__all__ = ["OllamaProvider", "LlamaVisionProvider", "SGLangProvider"]
