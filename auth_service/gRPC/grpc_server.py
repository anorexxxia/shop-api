import grpc
from di.container import container
from gRPC.grpc_routers import AuthGrpcService
from gRPC.interceptors import ErrorsInterceptor
from proto import auth_pb2_grpc


async def serve():
    # создаем сервер
    server = grpc.aio.server(interceptors=[ErrorsInterceptor()])

    # регистрируем наш сервис на сервере
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthGrpcService(container.storage, container.create_auth_service, container.jwt_service), server)

    # создаем порт для общения между приложениями
    server.add_insecure_port("[::]:50051")

    # стартуем сервер
    await server.start()

    print("Auth Service запущен на порту 50051")


    await server.wait_for_termination()