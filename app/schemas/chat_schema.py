from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    chat_session_id: Optional[str] = None
    query: str = None
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    chat_session_id: str
    response: str
