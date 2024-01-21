from pydantic import BaseModel
from typing import Optional

#DesignerChat api request and response
class DesignerChatRequest(BaseModel):
    query: Optional[str] = None
    context: Optional[dict] = None
    user: Optional[str] = None

class DesignerChatResponse(BaseModel):
    id: str
    response: str
    debug_data: Optional[dict] = None