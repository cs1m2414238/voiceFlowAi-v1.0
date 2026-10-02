import sys

from app.rag.loader import load_pdf
from app.rag.chunker import split_documents
from app.rag.embeddings import get_embedding_model
from app.rag.vector_store import create_vector_store


def ingest(pdf_path: str):
    documents = load_pdf(pdf_path)
    chunks = split_documents(documents)
    create_vector_store(chunks, get_embedding_model())
    print(f"Ingested {len(chunks)} chunks from {pdf_path}")


if __name__ == "__main__":
    ingest(sys.argv[1])