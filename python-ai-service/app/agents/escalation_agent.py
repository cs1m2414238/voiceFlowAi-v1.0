from datetime import datetime, timezone

from app.core.config import settings
from app.core.logging import get_logger
from app.integrations.java_backend_client import java_client

logger = get_logger(__name__)

DEFAULT_ESCALATION_MESSAGE = "Let me connect you with a human support representative."


def escalation_agent(
    question: str,
    reason: str = "human_requested",
    company_id: str = "default",
    session_id: str = "default",
) -> dict:
    """Handle escalation to a human support representative and optionally notify the Java backend."""
    payload = {
        "question": question,
        "reason": reason,
        "company_id": company_id,
        "session_id": session_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    logger.info("Escalating session=%s company=%s reason=%s", session_id, company_id, reason)

    if settings.JAVA_SYNC_ENABLED:
        java_client.sync_escalation(payload)

    return {
        "answer": DEFAULT_ESCALATION_MESSAGE,
        "escalated": True,
    }
