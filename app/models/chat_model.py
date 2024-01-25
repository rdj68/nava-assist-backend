from typing import List
from beanie import Document, Indexed
from vertexai.language_models import ChatMessage

class Chat(Document):
    user_id: str
    chat_session_id: Indexed(str)
    history: List[ChatMessage]

    @classmethod
    async def by_chat_id(cls, chat_id: str) -> "Chat":
        return await cls.find_one(cls.chat_id == chat_id)
    
    @classmethod
    async def by_user_id(cls, user_id: str) -> list["Chat"]:
        return await cls.find(cls.user_id == user_id)
    
    @classmethod
    async def by_user_id_and_chat_id(cls, user_id: str, chat_id: str) -> "Chat":
        return await cls.find_one(cls.user_id == user_id, cls.chat_id == chat_id)
    
    class Settings:
        collection = "chats"