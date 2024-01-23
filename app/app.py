from contextlib import asynccontextmanager
import os
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import vertexai
from app.core.config import settings
from app.models.user_model import User
from app.api.api_v1.router import main_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    initialize crucial application services 
    """
    os.environ.clear()
    load_dotenv(".env")
    db_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    vertexai.init()

    await init_beanie(database=db_client.get_database("nava-assist-backend"), document_models=[User])

    yield
    # os.environ.clear()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router, prefix=settings.API_V1_STR)
