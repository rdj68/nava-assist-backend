from typing import Any, Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    phone: str
    additional_info: Optional[Any] = None
    sessions: Optional[list[str]] = None
    token: Optional[str] = None
