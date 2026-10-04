from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.rag_routes import router as rag_router
from app.api.chat_routes import router as chat_router
from app.api.document_routes import router as document_router

app = FastAPI(
    title="VoiceFlow AI"
)

# Enable CORS so React frontend (port 5173) can communicate with FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint for React telemetry check
@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(rag_router)
app.include_router(chat_router)
app.include_router(document_router)