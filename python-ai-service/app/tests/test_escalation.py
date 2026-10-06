from app.agents import escalation_agent as esc


def test_escalation_returns_ticket():
    r = esc.escalation_agent("I want a person", "acme", "Intent: human")
    assert r["escalated"] is True
    assert r["ticket_id"].startswith("C-")


def test_escalation_survives_ticket_failure(monkeypatch):
    def broken(**kwargs):
        raise RuntimeError("store down")

    monkeypatch.setattr(esc, "create_ticket", broken)
    r = esc.escalation_agent("I want a person", "acme")
    assert r["escalated"] is True
    assert r["ticket_id"] is None