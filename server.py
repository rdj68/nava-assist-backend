from fastapi import FastAPI
from dotenv import load_dotenv
from aiModelClient.Clients import GeckoClient, BisonClient, GeminiClient
from controller import get_health_state
import schemas
import uuid
import logging
import os


app = FastAPI()
load_dotenv()

geckoClient = GeckoClient()
bisonClient = BisonClient()
geminiClient = GeminiClient()


@app.post("/v1/completions")
async def completion(request_body: schemas.CompletionRequest):
    logging.debug("Completion request received")
    prefix = request_body.segments.get("prefix", None)
    suffix = request_body.segments.get("suffix", None)

    response = await geckoClient.prompt(prefix, suffix=suffix)
    completion_response = get_completion_response(response.text)
    return completion_response


@app.get("/v1/health", response_model=schemas.HealthState)
def read_health():
    # Replace this with your function to get the health state
    health_state = get_health_state()
    return health_state


@app.post("/v1/chat", response_model=schemas.ChatResponse)
async def chat(request_body: schemas.chatRequest):
    user_query = request_body.userQuery
    context_params = request_body.context
    entireContent = {context_params.get(
        'entireContent', {})} if context_params else ''
    selectedContent = {context_params.get(
        'selectedContent', {})} if context_params else ''

    prompt = "{" + \
        f"query: {user_query}," + \
        "context_params: { " + \
        f"file_extension: {os.path.splitext(context_params.get('filePath', '')) if context_params else ''}," + \
        f"file_path: {context_params.get('filePath', {}) if context_params else ''}," + \
        f"selected_code: {selectedContent}," + \
        f"entire_code: {entireContent}," + \
        "if query is related to the context then consider whole expression as prompt otherwise consider only query as prompt" + \
        "}" + \
        "}"
    response = await bisonClient.prompt(prompt)
    chat_response = schemas.ChatResponse(
        id=str(uuid.uuid4()),
        response=response.text,
        debug_data=None
    )
    return chat_response


@app.post("/v1/designerchat", response_model=schemas.DesignerChatResponse)
async def designerchat(request_body: schemas.DesignerChatRequest):
    prompt = "{" + \
        f"message: {request_body.query}," + \
        f"context: {request_body.context}" + \
        "}"
    responses = await geminiClient.prompt(prompt)
    all_text_responses = []
    async for response in responses:
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.text:
                            all_text_responses.append(part.text)

    combined_response = ' '.join(all_text_responses)

    chat_response = schemas.DesignerChatResponse(
        id=str(uuid.uuid4()),
        response=combined_response,
    )

    return chat_response


# class SearchResponse(BaseModel):
#     num_hits: int
#     hits: List[dict]

# @app.get("/v1beta/search")
# async def search(q: str = Query(...), limit: Optional[int] = 20, offset: Optional[int] = 0):
#     # Your code here
#     pass


@app.post("/v1/events")
async def event(request_body: schemas.LogEventRequest):
    logging.debug(request_body)
    pass


def get_completion_response(text: str):
    choices = [{"index": 0, "text": text}]

    return schemas.CompletionResponse(id=str(uuid.uuid4()), choices=choices, debug_data=None)
