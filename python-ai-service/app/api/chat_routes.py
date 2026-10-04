from fastapi import APIRouter

from app.models.requests import ChatRequest
from app.models.responses import ChatResponse
from app.agents.faq_agent import faq_agent


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/ask", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer = faq_agent(request.question)

    return ChatResponse(
        answer=answer
    )