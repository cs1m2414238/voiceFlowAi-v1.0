from app.core.logging import get_logger
from app.llm.client import get_llm
from app.rag.qa import get_vectorstore
from app.rag.retriever import retrieve_documents

logger = get_logger(__name__)

DEFAULT_CATALOG_CONTEXT = (
    "Starter Plan: Best for individuals and small teams getting started with AI voice support. "
    "Pro Plan: Ideal for growing businesses needing multi-agent workflows, bookings, and order tracking. "
    "Enterprise Plan: Designed for large organizations requiring custom SLAs, dedicated support, and high volume."
)


def create_recommendation_prompt(context: str, question: str) -> str:
    return f"""
You are a helpful product and service recommendation specialist.
Use the context below to recommend the best option for the customer's needs.
Provide a clear, concise recommendation and explain why it fits.

Context:
{context}

Customer question:
{question}

Recommendation:
"""


def _retrieve_context(question: str) -> str:
    try:
        vectorstore = get_vectorstore()
        docs = retrieve_documents(vectorstore, question, k=3)
        if docs:
            joined = "\n\n".join(doc.page_content for doc in docs if getattr(doc, "page_content", ""))
            if joined.strip():
                return joined
    except Exception as exc:
        logger.debug("RAG context retrieval unavailable for recommendation, using default catalog: %s", exc)
    return DEFAULT_CATALOG_CONTEXT


def _fallback_recommendation(question: str) -> str:
    q = question.lower()
    if any(w in q for w in ("enterprise", "large", "company", "custom", "sla", "scale")):
        return (
            "Based on your needs, I recommend our Enterprise Plan, which includes custom SLAs, "
            "dedicated support, and full multi-agent voice and chat orchestration."
        )
    if any(w in q for w in ("small", "starter", "basic", "cheap", "budget", "individual", "personal")):
        return (
            "I recommend starting with our Starter Plan, which gives you core FAQ and voice assistant "
            "capabilities at an affordable tier."
        )
    return (
        "I recommend our Pro Plan, which offers the best balance of multi-agent support "
        "(FAQ, bookings, order tracking, and complaint handling) for most teams."
    )


def recommendation_agent(question: str, company_id: str = "default") -> dict:
    """Generate a tailored product or service recommendation using RAG context and the LLM."""
    context = _retrieve_context(question)
    prompt = create_recommendation_prompt(context, question)

    try:
        response = get_llm().invoke(prompt)
        answer = getattr(response, "content", str(response)).strip()
        if not answer:
            answer = _fallback_recommendation(question)
    except Exception as exc:
        logger.debug("LLM unavailable for recommendation (%s), using fallback recommendation: %s", company_id, exc)
        answer = _fallback_recommendation(question)

    return {
        "answer": answer,
        "escalated": False,
    }
