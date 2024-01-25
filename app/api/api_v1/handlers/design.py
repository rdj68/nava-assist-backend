from fastapi import APIRouter
import uuid
from app.services.ai_client import gemini_client
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.schemas.auth_schema import TokenPayload
from fastapi import Depends
from app.api.deps.auth_deps import authenticate


router = APIRouter()


@router.post("/designchat", response_model=ChatResponse)
async def designerchat(
    request_body: ChatRequest,
    tokenPayload: TokenPayload = Depends(authenticate),
):
    prompt = (
        "{"
        + f"message: {request_body.query},"
        + f"context: {request_body.context}"
        + "}"
    )
    responses = await gemini_client.prompt(prompt)
    all_text_responses = []
    async for response in responses:
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.text:
                            all_text_responses.append(part.text)

    combined_response = " ".join(all_text_responses)

    chat_response = ChatResponse(
        id=str(uuid.uuid4()),
        response=combined_response,
    )

    return chat_response
