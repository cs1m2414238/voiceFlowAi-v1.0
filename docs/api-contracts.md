# VoiceFlow AI — API Contracts

This document defines the REST API contracts between the **React Frontend**, **Java Spring Boot Backend** (`:8080`), and **Python FastAPI AI Service** (`:8000`).

---

## 1. Python AI Service (`http://localhost:8000`)

### `POST /agent/chat` — Multi-Agent LangGraph Orchestrator

Routes customer utterances through `ManagerAgent` to specialized domain agents (`faq`, `booking`, `order`, `complaint`, `recommendation`, `human`) with automatic confidence-based escalation.

**Request (JSON):**
| Field | Type | Notes |
|---|---|---|
| `question` | `string` | The customer's message (required) |
| `company_id` | `string` | Which company's knowledge base namespace to use |
| `session_id` | `string` | One per call or conversation |

**Response (JSON):**
| Field | Type | Notes |
|---|---|---|
| `answer` | `string` | Text to speak or display |
| `intent` | `string` | `faq`, `booking`, `order`, `complaint`, `recommendation`, `human` |
| `confidence` | `number` | `0.0` to `1.0` |
| `escalated` | `boolean` | `true` means hand over to a human agent |
| `ticket_id` | `string \| null` | Set when a complaint/escalation ticket is created |
| `booking_id` | `string \| null` | Set when a booking is confirmed |

> Field names use `snake_case`. Java DTOs map them with `@JsonProperty`.

---

### `POST /documents/upload` — PDF RAG Ingestion

Uploads a PDF document, extracts text via `pypdf`, splits into chunks (`500` chars, `50` overlap), embeds with HuggingFace `all-MiniLM-L6-v2`, and persists vectors to ChromaDB.

- **Request:** `multipart/form-data` with field `file` (`.pdf`)
- **Response (JSON):**
```json
{
  "message": "Document processed successfully.",
  "filename": "policy.pdf",
  "chunks_created": 64
}
```

---

### `POST /rag/ask` — Direct RAG Knowledge Base Query

- **Request (JSON):** `{ "question": "What is the return policy?" }`
- **Response (JSON):** `{ "answer": "Items can be returned within 30 days..." }`

---

## 2. Java Spring Boot Backend (`http://localhost:8080`)

### Authentication (`/api/auth`)

#### `POST /api/auth/register`
- **Request (JSON):**
```json
{
  "userName": "Priyanshu Sharma",
  "email": "admin@novamart.io",
  "password": "Password123",
  "role": "COMPANY_ADMIN",
  "companyId": "11111111-1111-1111-1111-111111111111"
}
```
- **Response (`201 Created`):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "userId": "aaaa1111-1111-1111-1111-111111111111",
  "userName": "Priyanshu Sharma",
  "email": "admin@novamart.io",
  "role": "COMPANY_ADMIN",
  "companyId": "11111111-1111-1111-1111-111111111111"
}
```

#### `POST /api/auth/login`
- **Request (JSON):** `{ "email": "admin@novamart.io", "password": "Password123" }`
- **Response (`200 OK`):** Same `AuthResponse` payload with JWT `token`.

---

### Companies (`/api/companies`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/companies` | Create a new tenant company (`companyName`, `industryType`, `supportEmail`, `supportPhone`) |
| `GET` | `/api/companies` | List all companies |
| `GET` | `/api/companies/{id}` | Get company by UUID |
| `PUT` / `PATCH` | `/api/companies/{id}` | Update company details |
| `DELETE` | `/api/companies/{id}` | Soft-delete (deactivate) a company (`204 No Content`) |

** Supported `IndustryType` values:** `CORPORATE`, `ECOMMERCE`, `HEALTHCARE`, `HOTEL`, `BANKING`, `EDUCATION`, `RESTAURANT`, `TRAVEL`, `OTHER`.

---

### Users (`/api/users`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/users` | Create a user |
| `GET` | `/api/users` | List all users |
| `GET` | `/api/users/{id}` | Get user by UUID |
| `PATCH` | `/api/users/{id}` | Update user |
| `DELETE` | `/api/users/{id}` | Soft-delete user |

---

### Conversations & Escalations (`/api/conversations`, `/api/escalations`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/conversations` | Start a new customer voice/chat session |
| `GET` | `/api/conversations` | List conversations (optional `?companyId=`) |
| `GET` | `/api/conversations/{id}` | Get conversation details |
| `POST` | `/api/conversations/{id}/messages` | Append a customer or AI agent message |
| `POST` | `/api/conversations/{id}/end` | Mark conversation `COMPLETED` |
| `GET` | `/api/escalations` | List escalated conversations / tickets |
| `POST` | `/api/escalations/{id}/resolve` | Resolve an open escalation |