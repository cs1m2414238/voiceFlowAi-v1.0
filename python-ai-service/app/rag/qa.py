from langchain_chroma import Chroma

from app.rag.embeddings import get_embedding_model
from app.rag.retriever import retrieve_documents
from app.llm.client import get_llm
from app.llm.prompts import create_rag_prompt
from app.llm.response_parser import parse_response

PERSIST_DIR = "./chroma_db"
NO_ANSWER = "I don't have that information in the knowledge base."

_vectorstore = None


def get_vector_store():
    """Load the saved ChromaDB once and reuse it."""
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=get_embedding_model(),
        )
    return _vectorstore


def answer_question(question: str) -> str:
    """Retrieve relevant chunks and answer using the LLM."""
    docs = retrieve_documents(get_vector_store(), question, k=3)

    if not docs:
        return NO_ANSWER

    context = "\n\n".join(doc.page_content for doc in docs)
    prompt = create_rag_prompt(context, question)
    response = get_llm().invoke(prompt)

    return parse_response(response)