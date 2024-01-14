from fastapi import FastAPI, Body, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from controller import get_health_state
from dotenv import load_dotenv
from aiModelClient.Clients import GeckoClient, BisonClient
import schemas
import uuid
import json

app = FastAPI()
load_dotenv()
geckoClient = GeckoClient()
bisonClient = BisonClient()

@app.post("/v1/completions")
async def completion(request_body: schemas.CompletionRequest):
    print("Completion request received.")
    prefix = request_body.segments.get("prefix", None) if request_body.segments else None
    suffix = request_body.segments.get("suffix", None) if request_body.segments else None
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
    user_query = request_body.query
    context_params = request_body.context
    user = request_body.user
    debug_options = request_body.debug_options

    # Build the prompt
    prompt_dict = {
        "query": user_query,
        "context_params": {
            "file_extension": {
                "value": context_params.get('file_extension', {}) if context_params else ''
            },
            "file_path": {
                "value": context_params.get('file_path', {}) if context_params else ''
            },
            "selected_code": {
                "value": context_params.get('selected_code', {}) if context_params else ''
            },
            "entire_code": {
                "value": context_params.get('entire_code', {}) if context_params else ''
            }
        },
        "user": user if user else '',
        "debug_options": debug_options if debug_options else {}
    }
    prompt = json.dumps(prompt_dict)
    response = await bisonClient.prompt(prompt)
    chat_response = schemas.ChatResponse(
        id = str(uuid.uuid4()),
        response=response.text,
        debug_data=None
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
    print(event)
    pass

# function to get completion response from text
def get_completion_response(text: str):
    choices = []
    choices.append({
        "index": 0,
        "text": text
    })

    completion_response = schemas.CompletionResponse(
        id = str(uuid.uuid4()),
        choices=choices,
        debug_data=None
    )

    return completion_response
