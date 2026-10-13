from typing import Protocol

from domain.models import User, UserResponse


class UserRepositoryInterface(Protocol):
    async def get_by_email(self, email: str) -> UserResponse | None:
        ...

    async def create(self, user: User) -> UserResponse:
        ...

    async def get_by_id(self, id: int) -> UserResponse | None:
        ...

    async def change_password(self, user_id: int, password: str):
        ...