from fastapi import APIRouter

from app.models.agent_state import AgentChatRequest, AgentChatResponse
from app.orchestration.graph import graph

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/chat", response_model=AgentChatResponse)
def agent_chat(request: AgentChatRequest):
    result = graph.invoke({
        "question": request.question,
        "company_id": request.company_id,
        "session_id": request.session_id,
    })
    return AgentChatResponse(
        answer=result["answer"],
        intent=result["intent"],
        confidence=result["confidence"],
        escalated=result["escalated"],
    )