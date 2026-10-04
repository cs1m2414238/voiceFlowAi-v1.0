from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api import agent_routes
from app.main import app
from app.models.agent_state import AgentChatResponse

client = TestClient(app)


def test_response_valid_without_ticket():
    r = AgentChatResponse(answer="hi", intent="faq", confidence=0.9, escalated=False)
    assert r.ticket_id is None


def test_response_valid_with_ticket():
    r = AgentChatResponse(
        answer="logged", intent="complaint", confidence=0.9,
        escalated=False, ticket_id="C-1001",
    )
    assert r.ticket_id == "C-1001"


def test_route_non_complaint_has_null_ticket(monkeypatch):
    fake = SimpleNamespace(invoke=lambda s: {
        "answer": "We open at 9.", "intent": "faq",
        "confidence": 0.9, "escalated": False,
    })
    monkeypatch.setattr(agent_routes, "graph", fake)

    body = client.post("/agent/chat", json={"question": "hours?"}).json()

    assert body["ticket_id"] is None


def test_route_complaint_returns_ticket(monkeypatch):
    fake = SimpleNamespace(invoke=lambda s: {
        "answer": "Logged.", "intent": "complaint", "confidence": 0.9,
        "escalated": False, "ticket_id": "C-1001",
    })
    monkeypatch.setattr(agent_routes, "graph", fake)

    body = client.post("/agent/chat", json={"question": "rude staff"}).json()

    assert body["ticket_id"] == "C-1001"