from typing import List
from pydantic import BaseModel, Field


# Health api response
class Version(BaseModel):
    build_date: str
    build_timestamp: str

    git_sha: str
    git_describe: str


class HealthState(BaseModel):
    model: str
    chat_model: str = Field(None)
    device: str
    arch: str
    cpu_info: str
    cpu_count: int
    cuda_devices: List[str]
    version: Version


class LogEventRequest(BaseModel):
    type: str
    completion_id: str
    choice_index: int


class SearchResponse(BaseModel):
    num_hits: int
    hits: List[dict]
