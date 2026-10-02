import itertools
from datetime import datetime, timezone

_counter = itertools.count(1001)
_TICKETS = []


def create_ticket(company_id, category, description, severity, customer_contact=None):
    """Mock ticket store. Replace with a call to the Java backend later."""
    ticket = {
        "ticket_id": f"C-{next(_counter)}",
        "company_id": company_id,
        "category": category,
        "description": description,
        "severity": severity,
        "status": "open",
        "customer_contact": customer_contact,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _TICKETS.append(ticket)
    return ticket