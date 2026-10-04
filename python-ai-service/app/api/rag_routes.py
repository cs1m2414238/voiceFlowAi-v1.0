from fastapi import APIRouter

from app.models.requests import RAGRequest
from app.models.responses import RAGResponse
from app.rag.qa import answer_question


router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


@router.post("/ask", response_model=RAGResponse)
def ask_question(request: RAGRequest):

    answer = answer_question(request.question)

    return RAGResponse(
        answer=answer
    )