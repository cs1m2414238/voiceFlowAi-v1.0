# VoiceFlow AI — Team Responsibilities & Module Ownership

VoiceFlow AI is architected as a modular microservices platform divided across four core engineering tracks:

---

## 1. Python AI, RAG & Multi-Agent Orchestration (`python-ai-service/`)

- **LangGraph Workflow & Routing (`app/orchestration/`, `app/agents/`):**
  - `ManagerAgent`: Intent classification (`faq`, `booking`, `order`, `complaint`, `recommendation`, `human`) and confidence scoring via Groq (`llama-3.1-8b-instant`).
  - Domain Agents: `FAQAgent`, `BookingAgent`, `OrderAgent`, `ComplaintAgent`, `RecommendationAgent`, and `EscalationAgent`.
  - Conditional routing and automatic human escalation when confidence `< 0.60` or on `complaint` / `human` intents.
- **RAG Pipeline (`app/rag/`, `app/api/document_routes.py`, `app/api/rag_routes.py`):**
  - PDF ingestion (`pypdf`), chunking (`RecursiveCharacterTextSplitter`), vector embeddings (`all-MiniLM-L6-v2`), and persistent storage (`ChromaDB`).
- **Business Tools (`app/tools/`):**
  - Automated ticket generation (`TKT-XXXXX`), booking confirmation (`BKG-XXXXX`), and order status lookup.

---

## 2. Java Spring Boot Core Backend (`javabackend/`)

- **Authentication & Security (`auth/`, `common/config/`):**
  - Stateless JWT authentication (`/api/auth/register`, `/api/auth/login`), BCrypt password hashing, and role-based access (`COMPANY_ADMIN`, `SUPPORT_AGENT`).
- **Multi-Tenant Domain Management (`company/`, `user/`, `customer/`):**
  - CRUD operations for tenant organizations (`/api/companies`), users (`/api/users`), and customers.
- **Conversation & Escalation Persistence (`conversation/`, `escalation/`, `order/`, `booking/`, `complaint/`):**
  - Tracking customer sessions, message logs, and human-in-the-loop escalations backed by PostgreSQL and Flyway migrations.

---

## 3. React + Tailwind Frontend Console (`frontend/`)

- **Agent Setup Wizard & Live Voice Sandbox (`src/App.jsx`, `src/components/AgentSetupWizard.jsx`):**
  - 4-step workflow builder for domain templates, PDF RAG ingestion, voice persona tuning, and real-time voice/text testing using Web Speech API + LangGraph.
- **Operations Console (`src/pages/`):**
  - `DashboardPage`: Live KPIs, intent distribution, and microservice health checks.
  - `ConversationPage`: Multi-turn session viewer with live intent, confidence, booking, ticket, and escalation badges.
  - `KnowledgeBasePage`: PDF upload & vector retrieval tester.
  - `CompanyPage`, `EscalationPage`, `LoginPage`, `RegisterPage`: Full tenant and operator management.
- **API Integration Layer (`src/api/`):**
  - `authApi.js`, `companyApi.js`, `conversationApi.js`, and `voiceApi.js` with Vite proxy and offline sandbox resilience.

---

## 4. Infrastructure, DevOps & Documentation (`infrastructure/`, `docs/`)

- **Containerization (`docker-compose.yml`, `Dockerfile`s):**
  - Multi-container orchestration for PostgreSQL, Java Backend, Python AI Service, React Frontend, and Nginx Reverse Proxy.
- **Database & Reverse Proxy (`infrastructure/postgres/init.sql`, `infrastructure/nginx/nginx.conf`):**
  - Automated schema initialization, seed data, and unified HTTP routing.
