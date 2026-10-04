import itertools
import threading
from datetime import datetime, timezone

from app.core.config import settings
from app.integrations.java_backend_client import java_client

# Mock data. Replace with calls to the Java backend's order module later.
ORDERS = {
    "1001": {"item": "Wireless headphones", "status": "Shipped", "date": "5 Oct"},
    "1002": {"item": "Running shoes", "status": "Processing", "date": "8 Oct"},
    "1003": {"item": "Water bottle", "status": "Delivered", "date": "1 Oct"},
}

# session_id -> {"kind": "status" | "request", "tries": int}
PENDING = {}

_lock = threading.Lock()
_counter = itertools.count(9001)
_REQUESTS = []


def get_order(order_id):
    order = ORDERS.get(order_id)
    if order is None and settings.JAVA_SYNC_ENABLED:
        order = java_client.get_order(order_id)
    return order


def create_service_request(order_id, kind):
    """Mock service request (cancellation or return) with optional Java sync."""
    with _lock:
        request = {
            "request_id": f"R-{next(_counter)}",
            "order_id": order_id,
            "kind": kind,
            "status": "open",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _REQUESTS.append(request)

    if settings.JAVA_SYNC_ENABLED:
        java_client.sync_order_request(request)

    return request