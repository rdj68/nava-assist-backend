from typing import Optional
from app.schemas.auth_schema import SignUpRequest
from app.models.user_model import User
from app.core.security import get_password, verify_password


class UserService:
    @staticmethod
    async def create_user(user: SignUpRequest):
        user_in = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password(user.password),
            phone=user.phone,
            additional_info=user.additional_info,
        )
        
        # Check if user already exists in db
        user = await UserService.get_user_by_email(email=user.email)
        if user is not None:
            return user
        
        await user_in.save()
        return user_in

    @staticmethod
    async def update_user(user: User):
        await user.save()
        return user

    @staticmethod
    async def authenticate_by_email(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None

        return user

    @staticmethod
    async def authenticate_by_phone(
        phone: str, password: str
    ) -> Optional[User]:
        user = await UserService.get_user_by_phone(phone=phone)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None

        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user

    @staticmethod
    async def get_user_by_phone(phone: str) -> Optional[User]:
        user = await User.find_one(User.phone == phone)
        return user

    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        user = await User.find_one(User.user_id == user_id)
        return user
