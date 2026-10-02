from typing import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    company_id: str
    session_id: str
    intent: str
    confidence: float
    answer: str
    escalated: bool