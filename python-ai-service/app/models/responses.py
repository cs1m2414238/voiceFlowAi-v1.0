from pydantic import BaseModel


class RAGResponse(BaseModel):
    answer: str


class ChatResponse(BaseModel):
    answer: str