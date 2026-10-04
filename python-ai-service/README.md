# VoiceFlow AI — Python AI Service

Multi-agent customer support orchestration, RAG document question-answering, and speech processing (STT/TTS) microservice built with **FastAPI**, **LangGraph**, **ChromaDB**, and **Ollama (`llama3.2:3b`)**.

## Architecture

- **Multi-Agent Orchestration (`app/orchestration/`, `app/agents/`)**:
  - `manager_agent`: Classifies customer intent (`faq`, `booking`, `order`, `complaint`, `recommendation`, `human`) with confidence scoring.
  - `faq_agent`: Answers company/policy questions using the ChromaDB RAG pipeline.
  - `booking_agent`: Multi-turn slot filling (`date`, `time`, `party_size`) with large-party escalation and cancellation support.
  - `order_agent`: Multi-turn order status lookup, cancellation (`Processing`), and return (`Delivered`) request creation.
  - `complaint_agent`: Categorizes complaints, detects high-risk keywords (with negation awareness), logs tickets, and escalates high-severity cases.
  - `recommendation_agent`: Suggests plans or products using RAG context with graceful fallback.
  - `escalation_agent`: Connects customers with a human representative when confidence is low or human support is requested.
- **RAG Pipeline (`app/rag/`)**:
  - PDF ingestion (`PyPDFLoader`), chunking (`RecursiveCharacterTextSplitter`), embeddings (`sentence-transformers/all-MiniLM-L6-v2`), and vector retrieval (`Chroma`).
- **Speech Processing (`app/speech/`)**:
  - Audio validation (`.wav`, `.mp3`, `.webm`, `.ogg`), speech-to-text (`/speech/stt`), and text-to-speech (`/speech/tts`).
- **Java Backend Integration (`app/integrations/java_backend_client.py`)**:
  - Optional non-blocking sync with the Spring Boot backend (`/api/complaints`, `/api/bookings`, `/api/orders`, `/api/escalations`).

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Service health check |
| `POST` | `/agent/chat` | Multi-agent routed chat (`AgentChatRequest` -> `AgentChatResponse`) |
| `POST` | `/chat/ask` | Direct FAQ chat endpoint |
| `POST` | `/rag/ask` | RAG knowledge base question answering |
| `POST` | `/documents/upload` | Upload and ingest a PDF document into ChromaDB |
| `POST` | `/speech/stt` | Transcribe uploaded audio file to text |
| `POST` | `/speech/tts` | Synthesize text into WAV audio (base64) |

## Quick Start

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Running Tests

```bash
pytest
```
