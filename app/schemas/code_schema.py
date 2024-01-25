from typing import List, Optional
from pydantic import BaseModel

# completion api request and response


class CompletionRequest(BaseModel):
    language: Optional[str] = None
    segments: Optional[dict] = None
    user: Optional[str] = None
    debug_options: Optional[dict] = None


class CompletionResponse(BaseModel):
    id: str
    choices: List[dict]
    debug_data: Optional[dict] = None
