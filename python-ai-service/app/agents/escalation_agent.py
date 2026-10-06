# app/agents/escalation_agent.py
import logging
from app.tools.tickets import create_ticket

logger = logging.getLogger(__name__)

def escalation_agent(question: str, company_id: str = "default", reason: str = "Low confidence / Human request") -> dict:
    """Handles explicit human escalation or fallback routing."""
    ticket_id = None
    try:
        ticket = create_ticket(
            company_id=company_id,
            category="other",
            description=f"Human Handoff Request: {question} (Reason: {reason})",
            severity="high"
        )
        ticket_id = ticket["ticket_id"]
    except Exception:
        logger.exception("Failed to auto-create escalation ticket")

    return {
        "answer": "I am connecting you with a human support representative. Please hold on.",
        "escalated": True,
        "ticket_id": ticket_id
    }