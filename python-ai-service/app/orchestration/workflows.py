from typing import Any
from app.orchestration.graph import graph
from app.orchestration.state import AgentState


def run_customer_support_workflow(
    question: str,
    company_id: str = "default",
    session_id: str = "default",
) -> dict[str, Any]:
    """Execute the multi-agent customer support workflow graph and return normalized state."""
    initial_state: AgentState = {
        "question": question,
        "company_id": company_id,
        "session_id": session_id,
    }
    result = graph.invoke(initial_state)
    return {
        "answer": result.get("answer", ""),
        "intent": result.get("intent", "human"),
        "confidence": float(result.get("confidence", 0.0)),
        "escalated": bool(result.get("escalated", False)),
        "ticket_id": result.get("ticket_id"),
        "booking_id": result.get("booking_id"),
    }
