from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    PROJECT_NAME: str = "NAVA-ASSIST-BACKEND"

    # Twilio
    TWILIO_ACCOUNT_SID: str = config("TWILIO_ACCOUNT_SID", cast=str)
    TWILIO_AUTH_TOKEN: str = config("TWILIO_AUTH_TOKEN", cast=str)
    TWILIO_SERVICE_SID: str = config("TWILIO_SERVICE_SID", cast=str)

    class Config:
        case_sensitive = True


settings = Settings()
