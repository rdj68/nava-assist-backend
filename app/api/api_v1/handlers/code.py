from fastapi import APIRouter
import uuid
import os
from app.services.ai_client import GeckoClient, BisonClient
from app.schemas.code_schema import CompletionRequest, CompletionResponse, ChatRequest, ChatResponse

router = APIRouter()
geckoClient = GeckoClient()
bisonClient = BisonClient()


@router.post("/completions")
async def completion(request_body: CompletionRequest):
    prefix = request_body.segments.get("prefix", None)
    suffix = request_body.segments.get("suffix", None)

    response = await geckoClient.prompt(prefix, suffix)
    completion_response = get_completion_response(response.text)
    return completion_response


@router.post("/chat", response_model=ChatResponse)
async def chat(request_body: ChatRequest):
    user_query = request_body.userQuery
    context_params = request_body.context
    entireContent = {context_params.get("entireContent", {})} if context_params else ""
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
    response = await bisonClient.prompt(prompt)
    chat_response = ChatResponse(
        id=str(uuid.uuid4()), response=response.text, debug_data=None
    )
    return chat_response


def get_completion_response(text: str):
    choices = [{"index": 0, "text": text}]
    return CompletionResponse(id=str(uuid.uuid4()), choices=choices, debug_data=None)
