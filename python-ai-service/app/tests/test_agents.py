from types import SimpleNamespace

from app.agents import booking_agent as booking_module
from app.agents import manager_agent as manager_module
from app.orchestration import graph as graph_module
from app.orchestration.graph import route_after_manager
from app.tools.bookings import ACTIVE


def fake_llm(text):
    return SimpleNamespace(invoke=lambda prompt: SimpleNamespace(content=text))


# ---- Manager ----
def test_manager_parses_valid_json(monkeypatch):
    monkeypatch.setattr(
        manager_module, "get_llm",
        lambda: fake_llm('{"intent": "faq", "confidence": 0.9}'),
    )
    assert manager_module.manager_agent("opening hours?") == {
        "intent": "faq", "confidence": 0.9,
    }


def test_manager_falls_back_to_human_on_garbage(monkeypatch):
    monkeypatch.setattr(manager_module, "get_llm", lambda: fake_llm("no idea"))
    assert manager_module.manager_agent("asdf")["intent"] == "human"


def test_manager_falls_back_to_human_when_llm_is_down(monkeypatch):
    def broken():
        raise ConnectionError("Ollama is down")

    monkeypatch.setattr(manager_module, "get_llm", broken)
    assert manager_module.manager_agent("hello")["intent"] == "human"


# ---- Routing ----
def test_low_confidence_escalates():
    assert route_after_manager({"intent": "faq", "confidence": 0.2}) == "escalation"


def test_human_intent_escalates():
    assert route_after_manager({"intent": "human", "confidence": 0.9}) == "escalation"


def test_confident_intent_goes_to_specialist():
    assert route_after_manager({"intent": "booking", "confidence": 0.9}) == "booking"


# ---- Booking agent ----
def test_booking_collects_details_then_confirms(monkeypatch):
    ACTIVE.clear()
    replies = iter([{"date": "Friday"}, {"time": "7 pm"}, {"party_size": 4}])
    monkeypatch.setattr(booking_module, "_extract", lambda m, known: next(replies))

    r1 = booking_module.booking_agent("book a table for Friday", "t1", "acme")
    assert "time" in r1["answer"].lower()

    r2 = booking_module.booking_agent("7 pm", "t1", "acme")
    assert "people" in r2["answer"].lower()

    r3 = booking_module.booking_agent("4 people", "t1", "acme")
    assert r3["booking_id"].startswith("B-")
    assert "t1" not in ACTIVE


def test_booking_large_party_escalates(monkeypatch):
    ACTIVE.clear()
    monkeypatch.setattr(
        booking_module, "_extract",
        lambda m, known: {"date": "Friday", "time": "7 pm", "party_size": 20},
    )
    r = booking_module.booking_agent("book for 20 people", "t2", "acme")
    assert r["escalated"] is True
    assert "t2" not in ACTIVE


def test_booking_can_be_cancelled(monkeypatch):
    ACTIVE.clear()
    ACTIVE["t3"] = {"date": "Friday"}
    r = booking_module.booking_agent("never mind", "t3", "acme")
    assert "cancelled" in r["answer"].lower()
    assert "t3" not in ACTIVE


# ---- Booking inside the graph ----
def test_booking_in_progress_skips_manager(monkeypatch):
    ACTIVE.clear()
    ACTIVE["s1"] = {"date": "Friday"}

    def manager_must_not_run(question):
        raise AssertionError("manager should not run mid-booking")

    monkeypatch.setattr(graph_module, "manager_agent", manager_must_not_run)
    monkeypatch.setattr(booking_module, "_extract", lambda m, known: {"time": "7 pm"})

    result = graph_module.graph.invoke({"question": "7 pm", "session_id": "s1"})

    assert result["intent"] == "booking"
    assert "people" in result["answer"].lower()
    ACTIVE.clear()