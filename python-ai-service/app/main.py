from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.rag_routes import router as rag_router
from app.api.chat_routes import router as chat_router
from app.api.agent_routes import router as agent_router
from app.api.document_routes import router as document_router
from app.api.speech_routes import router as speech_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="VoiceFlow AI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "UP",
        "service": "voiceflow-python-ai",
    }


app.include_router(rag_router)
app.include_router(chat_router)
app.include_router(agent_router)
app.include_router(document_router)
app.include_router(speech_router)