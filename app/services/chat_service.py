from vertexai.language_models import ChatMessage
from app.models.chat_model import Chat
from uuid import uuid4

class ChatService:
    
    @staticmethod
    async def create_chat(user_id: str, history: list[ChatMessage] ) -> Chat:
        chat_in = Chat(user_id= user_id, chat_session_id=str(uuid4()), history=history)
        
        await chat_in.save()
        return chat_in
    
    @staticmethod
    async def get_chat_by_session_id(chat_session_id: str) -> Chat:
        return await Chat.find_one(Chat.chat_session_id == chat_session_id)
    
    @staticmethod
    async def update_chat(chatSessionId: str, history: list[ChatMessage]):
        print("chat update function")
        chat = await Chat.find_one(Chat.chat_session_id == chatSessionId)
        
        
        await chat.update({"$set": {"history": history}})
        return chat
    
    @staticmethod
    async def get_chats_by_user_id(user_id: str) -> list[Chat]:
        return await Chat.find(Chat.user_id == user_id)