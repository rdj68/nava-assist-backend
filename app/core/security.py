from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Union, Any
from app.core.config import settings
from jose import jwt
from app.schemas.auth_schema import TokenResponse


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


# refresh token if it is going to expire in 5 days or less
async def refresh_token(token: str) -> TokenResponse:
    decoded_token = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
     # Convert exp claim to datetime object
    exp_datetime = datetime.utcfromtimestamp(decoded_token["exp"])
    if exp_datetime > datetime.utcnow() + timedelta(days=5):
        return TokenResponse(
            jwt_token=token, expires_in= decoded_token["exp"] - int(datetime.utcnow().timestamp())
        )

    token = create_access_token(decoded_token["sub"])
    token_response = TokenResponse(
        jwt_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return token_response


def get_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
