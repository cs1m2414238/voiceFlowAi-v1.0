from app.agents import complaint_agent as complaint_module
from app.orchestration import graph as graph_module


def test_graph_builds_without_duplicate_nodes():
    # build_graph() raises ValueError if a node is registered twice
    assert graph_module.build_graph() is not None


def test_faq_path(monkeypatch):
    monkeypatch.setattr(
        graph_module, "manager_agent",
        lambda q: {"intent": "faq", "confidence": 0.9},
    )
    monkeypatch.setattr(graph_module, "faq_agent", lambda q: "We open at 9 am.")

    result = graph_module.graph.invoke({"question": "What are your hours?"})

    assert result["intent"] == "faq"
    assert result["answer"] == "We open at 9 am."
    assert result["escalated"] is False


def test_complaint_path_creates_ticket(monkeypatch):
    monkeypatch.setattr(
        graph_module, "manager_agent",
        lambda q: {"intent": "complaint", "confidence": 0.9},
    )
    monkeypatch.setattr(
        complaint_module, "_analyse",
        lambda q: {"category": "service", "severity": "low", "summary": "Rude staff"},
    )

    result = graph_module.graph.invoke({"question": "The staff were rude"})

    assert result["intent"] == "complaint"
    assert result["ticket_id"].startswith("C-")
    assert result["escalated"] is False


def test_high_severity_complaint_escalates(monkeypatch):
    monkeypatch.setattr(
        graph_module, "manager_agent",
        lambda q: {"intent": "complaint", "confidence": 0.9},
    )
    monkeypatch.setattr(
        complaint_module, "_analyse",
        lambda q: {"category": "billing", "severity": "high", "summary": "Charged twice"},
    )

    result = graph_module.graph.invoke({"question": "I was charged twice"})

    assert result["escalated"] is True
    assert result["ticket_id"].startswith("C-")
    assert "human" in result["answer"].lower()


def test_low_confidence_goes_to_escalation_node(monkeypatch):
    monkeypatch.setattr(
        graph_module, "manager_agent",
        lambda q: {"intent": "faq", "confidence": 0.2},
    )

    result = graph_module.graph.invoke({"question": "asdf qwerty"})

    assert result["escalated"] is True
    assert "human" in result["answer"].lower()

def test_ticket_failure_is_preserved_through_graph(monkeypatch):
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

    result = graph_module.graph.invoke({"question": "The staff were rude"})

    assert result["ticket_id"] is None
    assert result["escalated"] is True
    assert "human" in result["answer"].lower()