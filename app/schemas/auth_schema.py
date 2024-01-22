from pydantic import BaseModel, EmailStr, Field
from typing import Any, Optional
from uuid import UUID


class SignUpRequest(BaseModel):
    email: EmailStr = Field(..., description="user email")
    username: str = Field(..., min_length=5, max_length=50, description="user username")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    phone: str = Field(..., min_length=10, max_length=10, description="user phone number")
    additional_info: Optional[Any] = None


class VerifyPhoneRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=10, description="user phone number")
    otp: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class SignUpResponse(BaseModel):
    status: str


class tokenResponse(BaseModel):
    jwt_token: str
    expires_in: int


class TokenPayload(BaseModel):
    sub: UUID = None
    expiry: int = None