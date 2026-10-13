from fastapi import Depends, Request
from fastapi.routing import APIRoute
from fastapi.security import HTTPBearer

security = HTTPBearer()

def authorized(func):
    func.requires_auth = True
    return func


class AuthRoute(APIRoute):
    async def _check_auth(self, request: Request):
        credentials = await security(request)
        auth_client = request.app.state.auth_client
        await auth_client.verify_token(credentials.credentials)
        request.state.token = credentials.credentials


class ProtectedRoute(AuthRoute):
    def __init__(self, *args, **kwargs):
        dependencies = kwargs.setdefault("dependencies", [])
        dependencies.append(Depends(security))

        super().__init__(*args, **kwargs)


    def get_route_handler(self):
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request):
            await self._check_auth(request)
            return await original_handler(request)

        return custom_handler


class AuthorizedRoute(AuthRoute):
    def __init__(self, *args, **kwargs):
        
        endpoint = kwargs.get("endpoint")

        if endpoint is not None and getattr(endpoint, "requires_auth", False):
            dependencies = kwargs.setdefault("dependencies", [])
            dependencies.append(Depends(security))

        super().__init__(*args, **kwargs)


    def get_route_handler(self):
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request):
            if getattr(self.endpoint, "requires_auth", False):
                await self._check_auth(request)

            return await original_handler(request)

        return custom_handler


