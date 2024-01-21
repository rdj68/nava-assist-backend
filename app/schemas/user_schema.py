from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Any

class UserOut(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    phone_number: str
    additional_info: Optional[Any] = None
    sessions: Optional[dict[str, list[UUID]]] = None
    disabled: Optional[bool] = False