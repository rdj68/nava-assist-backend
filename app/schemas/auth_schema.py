from pydantic import BaseModel, EmailStr, Field
from typing import Any

class SignUpRequest(BaseModel):
    email: EmailStr = Field(..., description="user email")
    username: str = Field(..., min_length=5, max_length=50, description="user username")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    phone_number: str
    additional_info: Any
    
class VerifyPhoneRequest(BaseModel):
    phone_number: str
    verification_code: str
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
class SignUpResponse(BaseModel):
    status: str

class tokenResponse(BaseModel):
    jwt_token: str
    expires_in: int

