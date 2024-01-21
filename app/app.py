from contextlib import asynccontextmanager
from beanie import init_beanie
from fastapi import FastAPI
from app.core.config import settings
from app.models.user_model import User
from motor.motor_asyncio import AsyncIOMotorClient
from app.api.api_v1.router import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    initialize crucial application services
    """

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).fodoist

    await init_beanie(database=db_client, document_models=[User])

    yield

    await db_client.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.include_router(main_router, prefix=settings.API_V1_STR)