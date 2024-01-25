from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    chat_id: Optional[str] = None
    query: str = None
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    chat_id: str
    response: str
