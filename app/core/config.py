from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    PROJECT_NAME: str = "NAVA-ASSIST-BACKEND"
    MONGO_URI: str = config("MONGO_URI", cast=str)

    class Config:
        case_sensitive = True


settings = Settings()
