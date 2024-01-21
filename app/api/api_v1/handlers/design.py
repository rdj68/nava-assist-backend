from fastapi import APIRouter
import uuid

from app.services.ai_client import GeminiClient
from app.schemas.design_schema import DesignerChatRequest, DesignerChatResponse


router = APIRouter()
geminiClient = GeminiClient()


@router.post("/designchat", response_model=DesignerChatResponse)
async def designerchat(request_body: DesignerChatRequest):
    prompt = (
        "{"
        + f"message: {request_body.query},"
        + f"context: {request_body.context}"
        + "}"
    )
    responses = await geminiClient.prompt(prompt)
    all_text_responses = []
    async for response in responses:
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.text:
                            all_text_responses.append(part.text)

    combined_response = " ".join(all_text_responses)

    chat_response = DesignerChatResponse(
        id=str(uuid.uuid4()),
        response=combined_response,
    )

    return chat_response
