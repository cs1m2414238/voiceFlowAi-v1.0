import itertools
import threading
from datetime import datetime, timezone

from app.core.config import settings
from app.integrations.java_backend_client import java_client

CATEGORIES = {"service", "product", "billing", "delivery", "other"}
SEVERITIES = {"low", "medium", "high"}

_lock = threading.Lock()
_counter = itertools.count(1001)
_TICKETS = []


def create_ticket(company_id, category, description, severity, customer_contact=None):
    """Mock ticket store (in memory, single process) with optional Java backend sync.

    Tickets and IDs are lost on restart unless synced to the Java backend's
    complaint module, which persists them in PostgreSQL.
    """
    if not company_id or not str(company_id).strip():
        raise ValueError("company_id is required")
    if category not in CATEGORIES:
        raise ValueError(f"Invalid category: {category!r}")
    if severity not in SEVERITIES:
        raise ValueError(f"Invalid severity: {severity!r}")
    if not description or not str(description).strip():
        raise ValueError("Description must not be empty")
    if customer_contact is not None and (
        not isinstance(customer_contact, str) or len(customer_contact) > 100
    ):
        raise ValueError("customer_contact must be a string of at most 100 characters")

    with _lock:
        ticket = {
            "ticket_id": f"C-{next(_counter)}",
            "company_id": company_id,
            "category": category,
            "description": str(description).strip(),
            "severity": severity,
            "status": "open",
            "customer_contact": customer_contact,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _TICKETS.append(ticket)

    if settings.JAVA_SYNC_ENABLED:
        java_client.sync_ticket(ticket)

    return ticket