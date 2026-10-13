from typing import Protocol

from domain.models import UserResponse


class TokenServiseInterface(Protocol):
    def create_token(self, user: UserResponse) -> str:
        ...

    def verify_token(self, token: str) -> dict:
        ...