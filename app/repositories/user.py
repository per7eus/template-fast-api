from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database.models import User

class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, login, password):
        user = User(login=login, password=password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)