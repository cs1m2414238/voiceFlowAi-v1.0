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

def test_health_endpoint():
       assert client.get("/health").json()["status"] == "UP"

def test_ticket_failure_through_real_graph_and_api(monkeypatch):
    from app.agents import complaint_agent as complaint_module
    from app.orchestration import graph as graph_module

    monkeypatch.setattr(
        graph_module, "manager_agent",
        lambda q: {"intent": "complaint", "confidence": 0.9},
    )
    monkeypatch.setattr(
        complaint_module, "_analyse",
        lambda q: {"category": "service", "severity": "low", "summary": "Rude staff"},
    )

    def broken_create_ticket(**kwargs):
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(complaint_module, "create_ticket", broken_create_ticket)

    response = client.post("/agent/chat", json={"question": "The staff were rude"})
    body = response.json()

    assert response.status_code == 200
    assert body["ticket_id"] is None
    assert body["escalated"] is True