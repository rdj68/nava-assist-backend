from typing import Any
from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError
from app.services.user_service import UserService
from app.schemas.auth_schema import (
    SignUpRequest,
    SignUpResponse,
    VerifyPhoneRequest,
    VerifyPhoneResponse,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse
)
from app.core.security import (create_access_token, refresh_token)
from app.core.config import settings
from app.services.twilio_service import TwilioService
from app.schemas.user_schema import User


auth_router = APIRouter()


@auth_router.post(
    "/signup",
    summary="Create account of user and send otp on the phone number",
    response_model=SignUpResponse,
)
async def signup(request: SignUpRequest) -> Any:
    try:

        # save the user
        await UserService.create_user(request)

        # send otp on phone number
        twilio_client = TwilioService(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
            settings.TWILIO_SERVICE_SID,
        )
        twilio_client.send_otp(request.phone)

    except ValidationError as ve:
        raise HTTPException(
            status_code=422, detail=f"Validation Error: {ve}") from ve
    except DuplicateKeyError as dke:
        raise HTTPException(
            status_code=409, detail=f"Duplicate Key Error: {dke}") from dke
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving item: {e}") from e

    return {"status": "success"}


@auth_router.post(
    "/verify", summary="Verify otp and return token", response_model=VerifyPhoneResponse
)
async def test_token(request: VerifyPhoneRequest) -> Any:
    #  verify otp
    try:
        twilioClient = TwilioService(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
            settings.TWILIO_SERVICE_SID,
        )
        twilioClient.verify_otp(request.phone, request.otp)
    except HTTPException as e:
        raise HTTPException(
            status_code=500, detail= "Error verifying OTP") from e

    # Fetch user from db
    user = await UserService.get_user_by_phone(request.phone)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid phone number")

    # generate token and update user
    token = create_access_token(user.user_id)
    user.token = token
    user.verified = True
    await UserService.update_user(user)

    verify_phone_response = VerifyPhoneResponse(user_id=user.user_id, username= user.username, email=user.email, jwt_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    return verify_phone_response.model_dump()


@auth_router.post(
    "/login", summary="Login user and get user info ", response_model=User
)
async def login(request: LoginRequest) -> Any:
    user = await UserService.authenticate_by_email(request.email, request.password)
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid email or password")

    return user


# endpoint to refresh token
@auth_router.post(
    "/refresh-token", summary="Refresh token", response_model=TokenResponse
)
async def refresh_token_handler(request: RefreshTokenRequest) -> Any:
    user = await UserService.get_user_by_id(request.user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid user id")

    user = await UserService.get_user_by_id(request.user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid user id")

    tokenResponse = await refresh_token(user.token)
    user.token = tokenResponse.jwt_token
    await UserService.update_user(user)

    return tokenResponse.model_dump()
