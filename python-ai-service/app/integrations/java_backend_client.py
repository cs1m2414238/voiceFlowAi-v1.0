from typing import Any, Optional
import httpx

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class JavaBackendClient:
    """HTTP client for syncing AI service state with the Java Spring Boot backend."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.base_url = (base_url or settings.JAVA_BACKEND_URL).rstrip("/")
        self.timeout = timeout if timeout is not None else settings.JAVA_BACKEND_TIMEOUT
        self.api_key = api_key if api_key is not None else settings.API_KEY

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def _request(
        self,
        method: str,
        path: str,
        json_data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Optional[dict[str, Any]]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            with httpx.Client(timeout=self.timeout, headers=self._headers()) as client:
                response = client.request(method=method, url=url, json=json_data, params=params)
                response.raise_for_status()
                if response.content:
                    return response.json()
                return {"status": "ok"}
        except Exception as exc:
            logger.debug("Java backend request failed (%s %s): %s", method, url, exc)
            return None

    def sync_ticket(self, ticket: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Sync a complaint ticket with `/api/complaints`."""
        return self._request("POST", "/api/complaints", json_data=ticket)

    def sync_booking(self, booking: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Sync a confirmed booking with `/api/bookings`."""
        return self._request("POST", "/api/bookings", json_data=booking)

    def get_order(self, order_id: str) -> Optional[dict[str, Any]]:
        """Fetch order details from `/api/orders/{order_id}`."""
        return self._request("GET", f"/api/orders/{order_id}")

    def sync_order_request(self, request_data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Sync an order cancellation/return service request with `/api/orders`."""
        return self._request("POST", "/api/orders", json_data=request_data)

    def sync_escalation(self, escalation_data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Notify Java backend of a human escalation at `/api/escalations`."""
        return self._request("POST", "/api/escalations", json_data=escalation_data)

    def health_check(self) -> bool:
        """Check whether the Java backend is reachable."""
        result = self._request("GET", "/actuator/health")
        return result is not None


java_client = JavaBackendClient()


def get_java_client() -> JavaBackendClient:
    return java_client
