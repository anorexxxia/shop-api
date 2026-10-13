from datasource.models.user import UserOrm
from domain.models import User, UserResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> UserResponse | None:
        user = select(UserOrm).where(UserOrm.email == email)
        user_orm = (await self.session.execute(user)).scalar_one_or_none()

        if not user_orm:
            return None
        return UserResponse.model_validate(user_orm)


    async def get_by_id(self, id: int) -> UserResponse | None:
        user = await self.session.get(UserOrm, id)

        if not user:
            return None
        return UserResponse.model_validate(user)
    
    
    async def create(self, user: User) -> UserResponse:
        new_user = UserOrm(**user.model_dump())
        
        self.session.add(new_user)
        await self.session.flush()

        return UserResponse.model_validate(new_user)


    async def change_password(self, user_id: int, password: str):
        query = update(UserOrm).where(UserOrm.id == user_id).values(password=password)
        await self.session.execute(query)