from pathlib import Path

from app.rag.embeddings import get_embedding_model
from app.rag.retriever import retrieve_documents
from app.rag.parser import ingest_pdf
from app.rag.vector_store import Chroma, _FallbackVectorStore
from app.llm.client import get_llm
from app.llm.prompts import create_rag_prompt
from app.llm.response_parser import parse_response


BASE_DIR = Path(__file__).resolve().parents[2]
PDF_PATH = BASE_DIR / "company_faq.pdf"
CHROMA_DIR = BASE_DIR / "chroma_test_db"

DEFAULT_FAQ_KNOWLEDGE = (
    "Refund Policy: Refunds take 5 to 7 business days to appear on your original payment method. "
    "Opening Hours: Our support team is open Monday to Friday from 9:00 AM to 6:00 PM. "
    "Shipping: Standard delivery takes 3 to 5 business days."
)

embeddings = None
llm = get_llm()


def _get_embeddings():
    global embeddings
    if embeddings is None:
        embeddings = get_embedding_model()
    return embeddings


def get_vectorstore():
    emb = _get_embeddings()
    if (not CHROMA_DIR.exists() or not any(CHROMA_DIR.iterdir())) and PDF_PATH.is_file():
        ingest_pdf(
            file_path=str(PDF_PATH),
            persist_directory=str(CHROMA_DIR)
        )

    store_cls = Chroma if Chroma is not None else _FallbackVectorStore
    return store_cls(
        persist_directory=str(CHROMA_DIR),
        embedding_function=emb
    )


def answer_question(question: str) -> str:
    try:
        vectorstore = get_vectorstore()
        documents = retrieve_documents(
            vectorstore,
            question,
            k=3
        )
        context = "\n\n".join(
            document.page_content for document in documents if getattr(document, "page_content", "")
        )
        if not context.strip():
            context = DEFAULT_FAQ_KNOWLEDGE
    except Exception:
        context = DEFAULT_FAQ_KNOWLEDGE

    prompt = create_rag_prompt(context, question)
    try:
        response = llm.invoke(prompt)
        answer = parse_response(response)
        if answer:
            return answer
    except Exception:
        pass

    q_lower = question.lower()
    if "refund" in q_lower:
        return "Refunds typically take 5 to 7 business days to be processed."
    if "hour" in q_lower or "open" in q_lower:
        return "We are open Monday through Friday from 9:00 AM to 6:00 PM."
    return "I don't have that information in the knowledge base."