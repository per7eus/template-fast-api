from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.session import get_session
from ..repositories.user import UserRepository
from ..services import user
from ..services.user import UserService
from ..schemas.user import UserSchema
user_router = APIRouter(prefix="/user", tags=["user"])

#для работы с классами сервиса и репозитория
def get_user_repository(sessions: AsyncSession = Depends(get_session)):
    return UserRepository(sessions)

def get_user_service(repository: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository)


@user_router.get("/")
async def get_user():
    return {"message": "Hello World"}

@user_router.post("/create")
async def create_user(user:UserSchema, service: UserService = Depends(get_user_service)):

    await service.create_user(user.login, user.password)
    return {"message": "User created"}