from fastapi import Request
from web.clients.auth_client import AuthClient


async def get_auth_client(request: Request) -> AuthClient:
    return request.app.state.auth_client

async def get_token(request: Request) -> str:
    return request.state.token