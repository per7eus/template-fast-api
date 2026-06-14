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

    async def find_user_by_login(self, login):
        query = select(User).where(User.login == login)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def find_user_by_id(self, user_id):
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
