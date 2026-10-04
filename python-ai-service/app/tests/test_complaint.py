from app.agents import complaint_agent as complaint_module
import pytest 
from types import SimpleNamespace

def test_fraud_mentioned_with_distant_negation_is_high_risk():
    text = "I am not saying this is fraud, but my money was stolen"
    assert complaint_module._has_high_risk(text) is True


def test_negated_scam_but_scammed_still_counts():
    assert complaint_module._has_high_risk("This is not a scam; I was scammed last week") is True


def test_negated_scam_alone_is_not_high_risk():
    assert complaint_module._has_high_risk("This is not a scam, just a late delivery") is False


@pytest.mark.parametrize("bad_reply", [
    "[1, 2, 3]", "null", "not json at all", "{broken", "", ["a", "list"], None,
])
def test_malformed_model_reply_falls_back(monkeypatch, bad_reply):
    fake = SimpleNamespace(invoke=lambda prompt: SimpleNamespace(content=bad_reply))
    monkeypatch.setattr(complaint_module, "get_llm", lambda: fake)

    result = complaint_module._analyse("My order arrived broken")

    assert result["category"] == "other"
    assert result["severity"] == "medium"

def test_llm_failure_still_creates_ticket(monkeypatch):
    def broken_llm():
        raise ConnectionError("Ollama is down")

    monkeypatch.setattr(complaint_module, "get_llm", broken_llm)

    result = complaint_module.complaint_agent("My order arrived broken", "acme")

    assert result["ticket_id"].startswith("C-")
    assert result["escalated"] is False


def test_ticket_failure_escalates_without_crashing(monkeypatch):
    monkeypatch.setattr(
        complaint_module, "_analyse",
        lambda q: {"category": "service", "severity": "low", "summary": "x"},
    )

    def broken_create_ticket(**kwargs):
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(complaint_module, "create_ticket", broken_create_ticket)

    result = complaint_module.complaint_agent("The staff were rude", "acme")

    assert result["ticket_id"] is None
    assert result["escalated"] is True
    assert "human" in result["answer"].lower()


def test_issue_does_not_trigger_sue():
    assert complaint_module._has_high_risk("I have an issue with my order") is False


def test_negated_fraud_is_not_high_risk():
    assert complaint_module._has_high_risk("This is not fraud, just a late delivery") is False


def test_real_threat_is_high_risk():
    assert complaint_module._has_high_risk("I will call my lawyer") is True


def test_other_risk_word_still_counts_after_negated_one():
    assert complaint_module._has_high_risk("It's not fraud but I will sue you") is True


def test_risk_keyword_marks_ticket_high(monkeypatch):
    monkeypatch.setattr(
        complaint_module, "_analyse",
        lambda q: {"category": "billing", "severity": "low", "summary": "Charged twice"},
    )
    result = complaint_module.complaint_agent("Charged twice, calling my lawyer", "acme")
    assert result["escalated"] is True

def test_valid_json_that_is_not_a_dict_falls_back(monkeypatch):
    fake = SimpleNamespace(invoke=lambda p: SimpleNamespace(content='{"x": 1}'))
    monkeypatch.setattr(complaint_module, "get_llm", lambda: fake)
    monkeypatch.setattr(complaint_module.json, "loads", lambda s: [1, 2, 3])

    result = complaint_module._analyse("My order arrived broken")

    assert result["category"] == "other"
    assert result["severity"] == "medium"