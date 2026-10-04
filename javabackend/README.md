# VoiceFlow AI - Java Backend

Spring Boot microservice for multi-tenant company management, JWT authentication, conversation orchestration, customer/booking/order/complaint/escalation persistence, and integration with the Python AI Service.

## Key Endpoints

- `POST /api/auth/register` & `POST /api/auth/login` - User registration & JWT authentication
- `GET/POST/PUT/PATCH/DELETE /api/companies` - Multi-tenant company CRUD
- `GET/POST/PATCH/DELETE /api/users` - User management
- `GET/POST/DELETE /api/customers` - Customer management
- `GET/POST /api/conversations` & `POST /api/conversations/{id}/messages` - Multi-turn AI conversation orchestration
- `POST /api/agents/chat`, `GET/POST /api/agents/config`, `POST /api/rag/upload` - Direct AI agent & RAG integration
- `GET/POST/PATCH /api/bookings`, `/api/orders`, `/api/complaints`, `/api/escalations` - Specialist domain modules
- `GET /api/health` - Combined Java Backend & Python AI Service health check

## Running Locally

```bash
./mvnw spring-boot:run
```
