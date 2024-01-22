from fastapi import APIRouter
from app.api.auth.jwt import auth_router
from app.api.api_v1.handlers import code, design, general

main_router = APIRouter()

main_router.include_router(auth_router, prefix='/auth', tags=["auth"])
main_router.include_router(code.router, prefix='', tags=["code"])
main_router.include_router(design.router, prefix='', tags=["design"])
main_router.include_router(general.router, prefix='', tags=["general"])