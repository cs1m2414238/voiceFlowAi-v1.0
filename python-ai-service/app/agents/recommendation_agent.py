import logging

from app.llm.client import get_llm
from app.llm.response_parser import parse_response
from app.rag.qa import get_vectorstore
from app.rag.retriever import retrieve_documents

logger = logging.getLogger(__name__)

NO_INFO = ("I don't have enough information to recommend something for that. "
           "Could you tell me more about what you're looking for?")


def _prompt(context: str, question: str) -> str:
    return f"""
You are a helpful shop assistant.
Recommend one to three items that fit the customer's request.
Use ONLY the items described in the context below. Do not invent items or prices.
For each item, give its name and one short reason it fits.
If nothing in the context fits, say you don't have a matching item.

Context:
{context}

Customer request:
{question}

Recommendation:
"""


def recommendation_agent(question: str, company_id: str = "default") -> dict:
    try:
        docs = retrieve_documents(get_vectorstore(), question, k=4)
        if not docs:
            return {"answer": NO_INFO, "escalated": False}

        context = "\n\n".join(d.page_content for d in docs)
        answer = parse_response(get_llm().invoke(_prompt(context, question)))
    except Exception:
        logger.exception("Recommendation failed")
        return {
            "answer": ("I'm having trouble looking that up right now. "
                       "Let me connect you with a team member."),
            "escalated": True,
        }

    return {"answer": answer or NO_INFO, "escalated": False}