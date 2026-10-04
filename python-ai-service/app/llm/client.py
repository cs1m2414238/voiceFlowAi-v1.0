from types import SimpleNamespace
import httpx

from app.core.config import settings

try:
    from langchain_ollama import ChatOllama
except ImportError:
    ChatOllama = None


class _FallbackOllamaClient:
    """Lightweight HTTP client for Ollama when langchain_ollama is not installed."""

    def __init__(self, model: str, base_url: str, temperature: float = 0.0):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature

    def invoke(self, prompt: str):
        try:
            with httpx.Client(timeout=5.0) as client:
                resp = client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": self.temperature},
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                return SimpleNamespace(content=data.get("response", ""))
        except Exception as exc:
            raise ConnectionError(f"Ollama is unreachable at {self.base_url}: {exc}") from exc


def get_llm():
    """
    Create and return the local Llama 3.2 model.
    """
    if ChatOllama is not None:
        return ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=settings.LLM_TEMPERATURE,
        )

    return _FallbackOllamaClient(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=settings.LLM_TEMPERATURE,
    )