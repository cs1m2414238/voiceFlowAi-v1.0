from types import SimpleNamespace
from fastapi.testclient import TestClient

from app.agents import recommendation_agent as rec_module
from app.agents.escalation_agent import escalation_agent
from app.main import app
from app.orchestration import graph as graph_module
from app.speech.audio_processor import generate_tone_wav_bytes

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP", "service": "voiceflow-python-ai"}


def test_stt_endpoint_transcribes_wav():
    wav_bytes = generate_tone_wav_bytes(duration_seconds=0.3)
    response = client.post(
        "/speech/stt",
        files={"file": ("sample.wav", wav_bytes, "audio/wav")},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["text"]) > 0
    assert body["language"] == "en"
    assert body["confidence"] > 0


def test_stt_endpoint_rejects_unsupported_format():
    response = client.post(
        "/speech/stt",
        files={"file": ("notes.txt", b"not audio", "text/plain")},
    )
    assert response.status_code == 400


def test_tts_endpoint_synthesizes_speech():
    response = client.post(
        "/speech/tts",
        json={"text": "Welcome to VoiceFlow AI support.", "voice": "Rachel"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["voice"] == "Rachel"
    assert body["format"] == "wav"
    assert len(body["audio_base64"]) > 0


def test_tts_endpoint_rejects_empty_text():
    response = client.post(
        "/speech/tts",
        json={"text": "   ", "voice": "Rachel"},
    )
    assert response.status_code == 400


def test_recommendation_agent_with_mock_llm(monkeypatch):
    monkeypatch.setattr(
        rec_module,
        "get_llm",
        lambda: SimpleNamespace(
            invoke=lambda prompt: SimpleNamespace(content="I suggest the Pro Plan for your team.")
        ),
    )
    result = rec_module.recommendation_agent("Which plan should I pick?", "acme")
    assert result["answer"] == "I suggest the Pro Plan for your team."
    assert result["escalated"] is False


def test_recommendation_agent_fallback_when_llm_down(monkeypatch):
    def broken_llm():
        raise ConnectionError("Ollama is down")

    monkeypatch.setattr(rec_module, "get_llm", broken_llm)
    result = rec_module.recommendation_agent("Which enterprise plan do you suggest?", "acme")
    assert "enterprise" in result["answer"].lower()
    assert result["escalated"] is False


def test_recommendation_node_in_graph(monkeypatch):
    monkeypatch.setattr(
        graph_module,
        "manager_agent",
        lambda q: {"intent": "recommendation", "confidence": 0.9},
    )
    monkeypatch.setattr(
        graph_module,
        "recommendation_agent",
        lambda q, c="default": {"answer": "We recommend the Pro Plan.", "escalated": False},
    )
    result = graph_module.graph.invoke({"question": "What plan do you suggest?"})
    assert result["intent"] == "recommendation"
    assert result["answer"] == "We recommend the Pro Plan."
    assert result["escalated"] is False


def test_escalation_agent_returns_human_handoff():
    result = escalation_agent("I need a human", reason="human_requested", company_id="acme")
    assert result["escalated"] is True
    assert "human" in result["answer"].lower()
