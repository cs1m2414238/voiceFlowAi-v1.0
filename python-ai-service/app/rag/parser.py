
from pathlib import Path

from app.rag.loader import load_pdf
from app.rag.chunker import split_documents
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import create_vector_store


def ingest_pdf(file_path: str, persist_directory: str):
    """
    Load a PDF, split it into chunks, create embeddings,
    and store the chunks in ChromaDB.
    """
    pdf_path = Path(file_path)

    if not pdf_path.is_file():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    documents = load_pdf(str(pdf_path))
    chunks = split_documents(documents)
    embeddings = get_embedding_model()

    vectorstore = create_vector_store(
        chunks,
        embeddings,
        persist_directory=persist_directory
    )

    return len(chunks), vectorstore