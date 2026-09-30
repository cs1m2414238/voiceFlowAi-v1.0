from app.rag.qa import answer_question


def faq_agent(question: str) -> str:
    """
    Answer a customer FAQ using the RAG pipeline.
    """

    answer = answer_question(question)

    return answer