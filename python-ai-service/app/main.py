from fastapi import FastAPI

from app.api.rag_routes import router as rag_router
from app.api.chat_routes import router as chat_router


app = FastAPI(
    title="VoiceFlow AI"
)


app.include_router(rag_router)
app.include_router(chat_router)