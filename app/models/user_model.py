from typing import Optional
from datetime import datetime
from uuid import uuid4
from beanie import Document, Indexed
from pydantic import Field, EmailStr

class User(Document):
    user_id: str = Field(default_factory= lambda: uuid4().hex)
    username: Indexed(str, unique=False)
    email: Indexed(EmailStr, unique=True)
    phone: Indexed(str, unique=True)
    hashed_password: str
    disabled: Optional[bool] = False
    sessions: Optional[list[str]] = None
    additional_info: Optional[dict[str, str]] = None
    token: Optional[str] = None
    verified: Optional[bool] = False
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False
    
    @property
    def create(self) -> datetime:
        return self.id.generation_time
    
    @classmethod
    async def by_email(self, email: str) -> "User":
        return await self.find_one(self.email == email)
    
    class Settings:
        collection = "users"

