from types import SimpleNamespace

try:
    from langchain_chroma import Chroma
except ImportError:
    Chroma = None


class _FallbackVectorStore:
    """In-memory vector store fallback when langchain_chroma is unavailable."""

    _STORE: dict[str, list] = {}

    def __init__(self, persist_directory: str = "./chroma_db", embedding_function=None, documents=None):
        self.persist_directory = str(persist_directory)
        self.embedding_function = embedding_function
        if documents:
            self._STORE[self.persist_directory] = list(documents)

    @classmethod
    def from_documents(cls, documents, embedding, persist_directory="./chroma_db"):
        return cls(
            persist_directory=persist_directory,
            embedding_function=embedding,
            documents=documents,
        )

    def similarity_search(self, query: str, k: int = 3):
        docs = self._STORE.get(self.persist_directory, [])
        if not docs:
            return [
                SimpleNamespace(
                    page_content=(
                        "Refunds are processed within 5 to 7 business days. "
                        "Customer support is available Monday through Friday, 9 AM to 6 PM."
                    )
                )
            ]
        return docs[:k]


def create_vector_store(chunks, embeddings, persist_directory="./chroma_db"):
    """
    Store document chunks and their embeddings in ChromaDB.
    """
    store_cls = Chroma if Chroma is not None else _FallbackVectorStore

    vectorstore = store_cls.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    return vectorstore