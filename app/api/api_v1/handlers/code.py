from uuid import uuid4
import os
from vertexai.language_models import ChatMessage
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps.auth_deps import authenticate
from app.services.ai_client import gecko_client, bison_client
from app.schemas.code_schema import (
    CompletionRequest,
    CompletionResponse
)
from app.schemas.chat_schema import (ChatRequest, ChatResponse)
from app.schemas.auth_schema import TokenPayload
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/completions", response_model=CompletionResponse)
async def completion(
    request_body: CompletionRequest, _ : TokenPayload = Depends(authenticate)
):
    prefix = request_body.segments.get("prefix", None)
    suffix = request_body.segments.get("suffix", None)

    response = await gecko_client.prompt(prefix, suffix)
    completion_response = get_completion_response(response.text)
    return completion_response


@router.post("/chat", response_model=ChatResponse)
async def code_chat(
    request_body: ChatRequest, token_payload: TokenPayload = Depends(authenticate)
):
    user_query = request_body.query
    context_params = request_body.context
    entireContent = {context_params.get(
        "entireContent", {})} if context_params else ""
    selectedContent = (
        {context_params.get("selectedContent", {})} if context_params else ""
    )

    prompt = (
        "{"
        + f"query: {user_query},"
        + "context_params: { "
        + f"file_extension: {os.path.splitext(context_params.get('filePath', '')) if context_params else ''},"
        + f"file_path: {context_params.get('filePath', {}) if context_params else ''},"
        + f"selected_code: {selectedContent},"
        + f"entire_code: {entireContent},"
        + "if query is related to the context then consider whole expression as prompt otherwise consider only query as prompt"
        + "}"
        + "}"
    )

    history = []
    chat = None
    
    # fetch chat history from database if chat_id is present
    if request_body.chat_id is not None:
        # fetch chat history from database
        chat = await ChatService.get_chat_by_session_id(request_body.chat_id)
        if chat is not None:
            history = chat.history

    # pass the history to bison client
    # NOTE: bison client will return response and update the history with the response and request
    response = await bison_client.prompt(prompt, history=history)
    
    if history == []:
        history.append(ChatMessage(author="user", content=user_query))
        history.append(ChatMessage(author="bot", content=response.text))
    print("prompt", prompt)
        

    try:
        if request_body.chat_id is not None:
            chat = await ChatService.update_chat(request_body.chat_id, history)
        else:
            chat = await ChatService.create_chat(token_payload["sub"], history=history)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving chat history: {e}") from e

    # return the response
    chat_response = ChatResponse(chat_id=chat.chat_session_id, response= response.text)
    return chat_response.model_dump()


def get_completion_response(text: str):
    choices = [{"index": 0, "text": text}]
    return CompletionResponse(id=str(uuid4()), choices=choices, debug_data=None)
