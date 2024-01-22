from fastapi import APIRouter, HTTPException
from typing import Any
from app.services.user_service import UserService
from app.schemas.auth_schema import SignUpRequest, SignUpResponse, VerifyPhoneRequest, tokenResponse
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError
from app.core.security import get_password, create_access_token
from app.core.config import settings


auth_router = APIRouter()


@auth_router.post('/signup', summary="Create account of user and send otp on the phone number", response_model= SignUpResponse)
async def login(request: SignUpRequest) -> Any:
    
    try:
        # hash the password before saving
        request.password = get_password(request.password)
        
        #TODO : send otp on phone number
        
        # save the user
        await UserService.create_user(request)
    except ValidationError as ve:
        return HTTPException(status_code=422, detail=f"Validation Error: {ve}")
    except DuplicateKeyError as dke:
        return HTTPException(status_code=409, detail=f"Duplicate Key Error: {dke}")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error saving item: {e}")
    
    return {"status" : "success"}


@auth_router.post('/verify', summary="Verify otp and return token", response_model=tokenResponse)
async def test_token(request: VerifyPhoneRequest) -> Any:

    #TODO : verify otp
    
    # Fetch user from db
    user = await UserService.get_user_by_phone(request.phone)
    
    # generate token
    token = create_access_token(user.user_id)
    
    return {"jwt_token" : token, "expires_in" : settings.ACCESS_TOKEN_EXPIRE_MINUTES}