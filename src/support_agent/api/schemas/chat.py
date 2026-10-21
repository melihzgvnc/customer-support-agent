from pydantic import BaseModel
from uuid import UUID, uuid4

class ChatRequest(BaseModel):
    query: str
    thread_id: UUID | None = None

class ChatResponse(BaseModel):
    thread_id: UUID | None = None
    answer: str