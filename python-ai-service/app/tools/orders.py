import itertools
import threading
from datetime import datetime, timezone

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
    return ORDERS.get(order_id)


def create_service_request(order_id, kind):
    """Mock service request (cancellation or return)."""
    with _lock:
        request = {
            "request_id": f"R-{next(_counter)}",
            "order_id": order_id,
            "kind": kind,
            "status": "open",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _REQUESTS.append(request)
    return request