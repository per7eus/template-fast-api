from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.session import get_session
from ..repositories.user import UserRepository
from ..services import user
from ..services.user import UserService
from ..schemas.user import UserSchema
from  ..database.models import User
from ..dependencies import get_current_user, get_user_repository, get_user_service


user_router = APIRouter(prefix="/user", tags=["user"])



@user_router.get("/")
async def get_user():
    return {"message": "Hello World"}

@user_router.post("/create")
async def create_user(user:UserSchema, service: UserService = Depends(get_user_service)):

    await service.create_user(user.login, user.password)
    return {"message": "User created"}

@user_router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
    "id": current_user.id,
    "login": current_user.login,
    "message": "Это защищенные данные!"
    }