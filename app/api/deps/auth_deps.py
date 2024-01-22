from fastapi import FastAPI, HTTPException, Request
from jose import JWTError, jwt
from app.core.config import settings
from app.schemas.auth_schema import TokenPayload

app = FastAPI()


# Dependency to validate JWT token
def authenticate(request: Request ) -> TokenPayload:
    token = request.headers.get("Authorization", None).removeprefix("Bearer ")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise credentials_exception
    return payload