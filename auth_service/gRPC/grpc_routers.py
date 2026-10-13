import grpc
from di.container import JWTService, Storage
from domain.services.auth_service import AuthService
from gRPC.mappers import (
    authorization_to_server,
    grpc_to_change_password_model,
    grpc_to_reset_password,
    request_to_user,
)
from proto import auth_pb2, auth_pb2_grpc


class AuthGrpcService(auth_pb2_grpc.AuthServiceServicer):
    def __init__(self, storage: Storage, service_factory, token_service: JWTService):
        self.storage = storage
        self.service_factory = service_factory
        self.token_service = token_service


    async def VerifyToken(self, request: auth_pb2.VerifyTokenRequest, context: grpc.aio.ServicerContext):
        self.token_service.verify_token(request.token)
        return auth_pb2.VerifyTokenResponse()

        
    async def Register(self, request: auth_pb2.RegisterRequest, context: grpc.aio.ServicerContext):
        new_user = request_to_user(request)

        async with self.storage.session() as session, session.begin():
                service: AuthService = self.service_factory(session)
                token = await service.register(new_user)
            
        return auth_pb2.RegisterResponse(token=token)


    async def Login(self, request: auth_pb2.LoginRequest, context: grpc.aio.ServicerContext):
        authorization = authorization_to_server(request)

        async with self.storage.session() as session:
            service: AuthService = self.service_factory(session)
            token = await service.login(authorization)

        return auth_pb2.LoginResponse(token=token)


    async def ChangePassword(self, request: auth_pb2.ChangePasswordRequest, context: grpc.aio.ServicerContext):
        authorization = dict(context.invocation_metadata()).get('authorization')
        request_to_service = grpc_to_change_password_model(request)

        async with self.storage.session() as session, session.begin():
            service: AuthService = self.service_factory(session)
            token = await service.change_password(authorization , request_to_service)

        return auth_pb2.ChangePasswordResponse(token=token)


    async def ResetPassword(self, request: auth_pb2.ResetPasswordRequest, context: grpc.aio.ServicerContext):
        email = grpc_to_reset_password(request)

        async with self.storage.session() as session, session.begin():
            service: AuthService = self.service_factory(session)
            await service.reset_password(email)

        return auth_pb2.ResetPasswordResponse(success=True)