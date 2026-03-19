"""LLM provider abstraction layer.

Import provider implementations so they register with the
LLMProviderFactory when the package is imported.
"""

# import providers to trigger registration
from .providers import ollama, sglang
