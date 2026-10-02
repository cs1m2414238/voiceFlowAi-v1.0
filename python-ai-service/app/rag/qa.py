
from pathlib import Path

from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model
from app.rag.retriever import retrieve_documents
from app.rag.parser import ingest_pdf
from app.llm.client import get_llm
from app.llm.prompts import create_rag_prompt
from app.llm.response_parser import parse_response


BASE_DIR = Path(__file__).resolve().parents[2]
PDF_PATH = BASE_DIR / "company_faq.pdf"
CHROMA_DIR = BASE_DIR / "chroma_test_db"

embeddings = get_embedding_model()
llm = get_llm()


def get_vectorstore():
    if not CHROMA_DIR.exists() or not any(CHROMA_DIR.iterdir()):
        ingest_pdf(
            file_path=str(PDF_PATH),
            persist_directory=str(CHROMA_DIR)
        )

    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings
    )


def answer_question(question: str) -> str:
    vectorstore = get_vectorstore()

    documents = retrieve_documents(
        vectorstore,
        question,
        k=3
    )

    context = "\n\n".join(
        document.page_content for document in documents
    )

    prompt = create_rag_prompt(context, question)
    response = llm.invoke(prompt)

    return parse_response(response)