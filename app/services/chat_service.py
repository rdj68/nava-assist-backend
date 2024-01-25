from uuid import uuid4
from vertexai.language_models import ChatMessage
from app.models.chat_model import Chat


class ChatService:
    """
    Service class for managing chat operations.
    """

    @staticmethod
    async def create_chat(user_id: str, history: list[ChatMessage]) -> Chat:
        """
        Creates a new chat with the given user ID and chat history.

        Args:
            user_id (str): The ID of the user associated with the chat.
            history (list[ChatMessage]): The chat history is a list of ChatMessage(defined in vertexai sdk)

        Returns:
            Chat: The created chat object.
        """
        chat_in = Chat(user_id=user_id, chat_session_id=str(
            uuid4()), history=history)

        await chat_in.save()
        return chat_in

    @staticmethod
    async def get_chat_by_session_id(chat_session_id: str) -> Chat:
        """
        Retrieves a chat by its session ID.

        Args:
            chat_session_id (str): The session ID of the chat.

        Returns:
            Chat: The chat object.
        """
        return await Chat.find_one(Chat.chat_session_id == chat_session_id)

    @staticmethod
    async def append_message_to_chat(chat_session_id: str, messages_to_push: list[ChatMessage]):
        """
        Appends messages to the chat history.

        Args:
            chat_session_id (str): The session ID of the chat.
            messages_to_push (list[ChatMessage]): The messages to append.

        Returns:
            Chat: The updated chat object.
        """
        chat = await Chat.find_one(Chat.chat_session_id == chat_session_id)

        await chat.update({"$push": {"history": {"$each": messages_to_push}}})
        return chat

    @staticmethod
    async def get_chats_by_user_id(user_id: str) -> list[Chat]:
        """
        Retrieves all chats associated with a user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list[Chat]: A list of chat objects.
        """
        return await Chat.find(Chat.user_id == user_id)
