from app.agents import complaint_agent as complaint_module


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