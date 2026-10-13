from fastapi import APIRouter, Body, Depends
from proto import auth_pb2
from pydantic import EmailStr
from web.clients.auth_client import AuthClient
from web.dependencies.authorization import get_auth_client, get_token
from web.middleware import AuthorizedRoute, authorized
from web.models.auth import ChangePasswordRequest, RequestUser, UserLogin

auth_router = APIRouter(tags=['authorization'], route_class=AuthorizedRoute)


@auth_router.patch(
    "/change_password",
    summary="Смена пароля",
    description="Возвращает статус и новый токен",
)
@authorized
async def change_password(psw: ChangePasswordRequest, token: str = Depends(get_token),
                          auth_client: AuthClient = Depends(get_auth_client)):
    response: auth_pb2.ChangePasswordResponse = await auth_client.change_password(psw, token)
    return {"success": "ok", "token": response.token}


@auth_router.post(
    "/reset",
    summary="Сброс пароля",
    description="Возвращает новый сгенерированный пароль в консоль приложения авторизации"
)
async def reset_password(email: EmailStr = Body(), auth_client: AuthClient = Depends(get_auth_client)):
    response: auth_pb2.ResetPasswordResponse = await auth_client.reset_password(email)
    return {"success": response.success}


@auth_router.post(
    "/auth",
    summary="Авторизация",
    description="Возвращает токен авторизации",
    response_description="Возвращает токен авторизации"
)
async def auth(user_login: UserLogin, auth_client: AuthClient = Depends(get_auth_client)):
    response: auth_pb2.LoginResponse = await auth_client.login(user_login)
    return {"token": response.token}


@auth_router.post(
    "/register",
    summary="Регистрация",
    description="Возвращает токен зарегистрированного пользователя"
)
async def register(user: RequestUser, auth_client: AuthClient = Depends(get_auth_client)):
    response: auth_pb2.RegisterResponse = await auth_client.register(user)
    return {"token": response.token}