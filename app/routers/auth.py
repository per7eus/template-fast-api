from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..repositories.user import UserRepository
from ..services.auth import AuthService
from ..database.session import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


auth_router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_repository(sessions: AsyncSession = Depends(get_session)):
    return UserRepository(sessions)


async def get_auth_service(repository: UserRepository = Depends(get_user_repository)):
    return AuthService(repository)


@auth_router.post("/login")
async def login(from_data: OAuth2PasswordRequestForm = Depends(),auth_service: AuthService = Depends(get_auth_service)):
    login = from_data.username
    password = from_data.password

    user = await auth_service.authenticate_user(login, password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token =  auth_service.creat_access_token(data={"sub": str(user.id)})

    return {"status": True ,"access_token": access_token, "token_type": "bearer"}
