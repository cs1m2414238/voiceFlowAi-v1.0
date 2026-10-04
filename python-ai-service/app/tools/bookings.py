import itertools
from datetime import datetime, timezone

from app.core.config import settings
from app.integrations.java_backend_client import java_client

_counter = itertools.count(5001)
_BOOKINGS = []

# session_id -> details collected so far (date, time, party_size)
ACTIVE = {}


def create_booking(company_id, date, time, party_size):
    """Mock booking store with optional Java backend sync."""
    booking = {
        "booking_id": f"B-{next(_counter)}",
        "company_id": company_id,
        "date": date,
        "time": time,
        "party_size": party_size,
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _BOOKINGS.append(booking)

    if settings.JAVA_SYNC_ENABLED:
        java_client.sync_booking(booking)

    return booking