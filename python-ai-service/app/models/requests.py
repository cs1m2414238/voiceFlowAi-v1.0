from pydantic import BaseModel


class RAGRequest(BaseModel):
    question: str


class ChatRequest(BaseModel):
    question: str