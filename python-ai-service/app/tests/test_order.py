from app.agents import order_agent as order_module
from app.orchestration import graph as graph_module
from app.tools.orders import PENDING


def setup_function():
    PENDING.clear()


def test_status_with_order_number():
    r = order_module.order_agent("Where is order 1001?", "s1")
    assert "shipped" in r["answer"].lower()
    assert r["escalated"] is False


def test_asks_for_number_then_answers():
    r1 = order_module.order_agent("Where is my order?", "s2")
    assert "order number" in r1["answer"].lower()
    assert "s2" in PENDING

    r2 = order_module.order_agent("1003", "s2")
    assert "delivered" in r2["answer"].lower()
    assert "s2" not in PENDING


def test_unknown_order_then_handoff():
    r1 = order_module.order_agent("order 9999", "s3")
    assert "couldn't find" in r1["answer"].lower()
    order_module.order_agent("order 9998", "s3")
    r3 = order_module.order_agent("order 9997", "s3")
    assert r3["escalated"] is True
    assert "s3" not in PENDING


def test_cancel_processing_order_creates_request():
    r = order_module.order_agent("cancel order 1002", "s4")
    assert "R-" in r["answer"]
    assert "cancellation" in r["answer"].lower()


def test_cancel_shipped_order_is_refused():
    r = order_module.order_agent("cancel order 1001", "s5")
    assert "already shipped" in r["answer"].lower()
    assert "R-" not in r["answer"]


def test_return_delivered_order_creates_request():
    r = order_module.order_agent("I want to return order 1003", "s6")
    assert "R-" in r["answer"]


def test_never_mind_drops_the_request():
    order_module.order_agent("Where is my order?", "s7")
    r = order_module.order_agent("never mind", "s7")
    assert "s7" not in PENDING
    assert "dropped" in r["answer"].lower()


def test_pending_order_skips_manager_in_graph(monkeypatch):
    PENDING["s8"] = {"kind": "status", "tries": 1}

    def manager_must_not_run(question):
        raise AssertionError("manager should not run mid-order")

    monkeypatch.setattr(graph_module, "manager_agent", manager_must_not_run)

    result = graph_module.graph.invoke({"question": "1001", "session_id": "s8"})

    assert result["intent"] == "order"
    assert "shipped" in result["answer"].lower()