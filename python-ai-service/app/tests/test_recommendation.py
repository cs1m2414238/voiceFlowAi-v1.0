from types import SimpleNamespace

from app.agents import recommendation_agent as rec
from app.orchestration import graph as graph_module


def fake_llm(text):
    return SimpleNamespace(invoke=lambda prompt: SimpleNamespace(content=text))


def patch_catalog(monkeypatch, docs):
    monkeypatch.setattr(rec, "get_vectorstore", lambda: object())
    monkeypatch.setattr(rec, "retrieve_documents", lambda store, q, k=4: docs)


def test_recommends_from_catalog(monkeypatch):
    patch_catalog(monkeypatch, [SimpleNamespace(page_content="Trail shoes, Rs 3000")])
    monkeypatch.setattr(rec, "get_llm", lambda: fake_llm("I suggest the trail shoes."))

    result = rec.recommendation_agent("shoes for hiking", "acme")

    assert "trail shoes" in result["answer"].lower()
    assert result["escalated"] is False


def test_no_matching_documents_asks_for_detail(monkeypatch):
    patch_catalog(monkeypatch, [])

    result = rec.recommendation_agent("something", "acme")

    assert result["answer"] == rec.NO_INFO
    assert result["escalated"] is False


def test_empty_llm_answer_uses_fallback(monkeypatch):
    patch_catalog(monkeypatch, [SimpleNamespace(page_content="Water bottle")])
    monkeypatch.setattr(rec, "get_llm", lambda: fake_llm("   "))

    assert rec.recommendation_agent("a bottle", "acme")["answer"] == rec.NO_INFO


def test_failure_escalates_to_human(monkeypatch):
    def broken():
        raise ConnectionError("Ollama is down")

    patch_catalog(monkeypatch, [SimpleNamespace(page_content="Water bottle")])
    monkeypatch.setattr(rec, "get_llm", broken)

    result = rec.recommendation_agent("a bottle", "acme")

    assert result["escalated"] is True
    assert "team member" in result["answer"].lower()


def test_prompt_limits_answer_to_context():
    prompt = rec._prompt("Trail shoes", "shoes for hiking")
    assert "Trail shoes" in prompt
    assert "shoes for hiking" in prompt
    assert "ONLY" in prompt


def test_recommendation_route_in_graph(monkeypatch):
    monkeypatch.setattr(
        graph_module, "manager_agent",
        lambda q: {"intent": "recommendation", "confidence": 0.9},
    )
    monkeypatch.setattr(
        graph_module, "recommendation_agent",
        lambda q, c: {"answer": "Try the trail shoes.", "escalated": False},
    )

    result = graph_module.graph.invoke({"question": "which shoes?"})

    assert result["intent"] == "recommendation"
    assert result["answer"] == "Try the trail shoes."