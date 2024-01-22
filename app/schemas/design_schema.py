from typing import Optional
from pydantic import BaseModel

# DesignerChat api request and response


class DesignerChatRequest(BaseModel):
    query: Optional[str] = None
    context: Optional[dict] = None
    user: Optional[str] = None


class DesignerChatResponse(BaseModel):
    id: str
    response: str
    debug_data: Optional[dict] = None
