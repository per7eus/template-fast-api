from ..repositories.user import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.UserRepository = repository

    async def create_user(self, login: str, password: str):
        return await self.UserRepository.create_user(login, password)