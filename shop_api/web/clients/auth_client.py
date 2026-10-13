from proto import auth_pb2, auth_pb2_grpc
from web.models.auth import ChangePasswordRequest, RequestUser, UserLogin


class AuthClient:
    def __init__(self, channel):
        # клиентская заглушка, для вызова функций на удаленном сервере
        self.stub = auth_pb2_grpc.AuthServiceStub(channel)


    async def verify_token(self, token: str):
        return await self.stub.VerifyToken(auth_pb2.VerifyTokenRequest(token=token))


    async def register(self, user: RequestUser):
        return await self.stub.Register(auth_pb2.RegisterRequest(**user.model_dump()))


    async def login(self, user: UserLogin):
        return await self.stub.Login(auth_pb2.LoginRequest(**user.model_dump()))


    async def change_password(self, psw: ChangePasswordRequest, token: str):
        metadata = (("authorization", token),)
        return await self.stub.ChangePassword(auth_pb2.ChangePasswordRequest(**psw.model_dump()), metadata=metadata)


    async def reset_password(self, email):
        return await self.stub.ResetPassword(auth_pb2.ResetPasswordRequest(email=email))