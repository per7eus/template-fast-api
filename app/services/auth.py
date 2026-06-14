from datetime import datetime, timedelta, timezone

from jose import jwt

from app.repositories.user import UserRepository


SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10000000


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def authenticate_user(self, login: str, password: str):
        user = await self.repository.find_user_by_login(login)
        if not user:
            return False

        if user.password != password:
            return False

        return user

    def creat_access_token(self, data: dict):
        to_encode = data.copy()
        expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expires})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt