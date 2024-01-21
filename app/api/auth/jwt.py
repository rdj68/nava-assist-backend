from fastapi import APIRouter, Depends, HTTPException
from typing import Any

from app.services.user_service import UserService
from app.schemas.auth_schema import SignUpRequest, SignUpResponse
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError


auth_router = APIRouter()


@auth_router.post('/signup', summary="Create access and refresh tokens for user", response_model= SignUpResponse)
async def login(request: SignUpRequest = Depends()) -> Any:
    
    try: 
        user = await UserService.create_user(request)
    except ValidationError as ve:
        return HTTPException(status_code=422, detail=f"Validation Error: {ve}")
    except DuplicateKeyError as dke:
        return HTTPException(status_code=409, detail=f"Duplicate Key Error: {dke}")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error saving item: {e}")
    
    return {"status" : "success"}


# @auth_router.post('/', summary="Test if the access token is valid", response_model=UserOut)
# async def test_token(user: User = Depends(get_current_user)):
#     return user


# @auth_router.post('/refresh', summary="Refresh token", response_model=TokenSchema)
# async def refresh_token(refresh_token: str = Body(...)):
#     try:
#         payload = jwt.decode(
#             refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     user = await UserService.get_user_by_id(token_data.sub)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid token for user",
#         )
#     return {
#         "access_token": create_access_token(user.user_id),
#         "refresh_token": create_refresh_token(user.user_id),
#     }