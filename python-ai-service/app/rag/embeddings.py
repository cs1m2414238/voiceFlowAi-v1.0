try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    HuggingFaceEmbeddings = None


class _FallbackEmbeddings:
    """Deterministic lightweight embeddings fallback when langchain_huggingface is unavailable."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        vec = [0.0] * 16
        for idx, ch in enumerate(text.lower()):
            vec[idx % 16] += (ord(ch) % 31) / 31.0
        return vec


def get_embedding_model():
    """
    Load and return the embedding model.
    """
    if HuggingFaceEmbeddings is not None:
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _FallbackEmbeddings()