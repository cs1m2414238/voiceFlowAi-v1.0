from pydantic import BaseModel


class AgentChatRequest(BaseModel):
    question: str
    company_id: str = "default"
    session_id: str = "default"


class AgentChatResponse(BaseModel):
    answer: str
    intent: str
    confidence: float
    escalated: bool
    ticket_id: str | None = None