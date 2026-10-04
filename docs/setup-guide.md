# VoiceFlow AI — Local & Docker Setup Guide

## Prerequisites

- **Node.js** `>= 18.x` and `npm` (for `frontend/`)
- **Java JDK** `21` and **Maven** (`./mvnw` wrapper included in `javabackend/`)
- **Python** `>= 3.10` and `pip` (for `python-ai-service/`)
- **PostgreSQL** `15+` (or **Docker Desktop** for containerized setup)
- **Groq API Key** (`GROQ_API_KEY`) for `llama-3.1-8b-instant` LLM inference

---

## Option 1: Quick Start with Docker Compose

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
   Set your `GROQ_API_KEY` inside `.env`.

2. Build and start all microservices:
   ```bash
   docker-compose up --build
   ```

3. Access the services:
   - **Frontend UI (Vite / Nginx):** `http://localhost:5173` (or `http://localhost:80`)
   - **Java Spring Boot API:** `http://localhost:8080`
   - **Python FastAPI Swagger Docs:** `http://localhost:8000/docs`
   - **PostgreSQL Database:** `localhost:5432` (`voiceflow_db`)

---

## Option 2: Running Services Individually (Local Development)

### 1. Python AI & LangGraph Service (`Port 8000`)

```bash
cd python-ai-service
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# macOS / Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

Create `python-ai-service/.env` with:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```

Run the Python test suite:
```bash
pytest
```

---

### 2. Java Spring Boot Backend (`Port 8080`)

Ensure PostgreSQL is running locally with database `voiceflow_db` (or run `docker-compose up -d postgres`).

```bash
cd javabackend
./mvnw spring-boot:run
```

---

### 3. React + Vite Frontend (`Port 5173`)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser. Vite automatically proxies `/api` requests to `http://localhost:8080` and `/agent`, `/rag`, `/documents`, `/speech`, `/chat` requests to `http://localhost:8000`.
