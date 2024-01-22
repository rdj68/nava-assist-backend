from typing import Any, Optional
from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    email: EmailStr = Field(..., description="user email")
    username: str = Field(..., min_length=5, max_length=50,
                          description="user username")
    password: str = Field(..., min_length=5, max_length=24,
                          description="user password")
    phone: str = Field(..., min_length=10, max_length=10,
                       description="user phone number")
    additional_info: Optional[Any] = None


class VerifyPhoneRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=10,
                       description="user phone number")
    otp: str


class VerifyPhoneResponse(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    jwt_token: str
    expires_in: int


class RefreshTokenRequest(BaseModel):
    user_id: str


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24,
                          description="user password")


class SignUpResponse(BaseModel):
    status: str


class TokenResponse(BaseModel):
    jwt_token: str
    expires_in: int


class TokenPayload(BaseModel):
    sub: str = None
    expiry: int = None
