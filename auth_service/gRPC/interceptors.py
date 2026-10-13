import grpc
from domain.exceptions import (
    InvalidCredentialsError,
    InvalidOldPasswordError,
    UserNotFoundError,
)
from grpc.aio import ServerInterceptor
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


class ErrorsInterceptor(ServerInterceptor):
    """Перехватывает ошибки RPC и превращает их в статусы gRPC."""
    async def intercept_service(self, continuation, handler_call_details):
        # вызываемые наши методы в RPC
        handler = await continuation(handler_call_details)

        if handler is None:
            return None

        # мы используем только один - один, есть еще один - многие, многие - один, многие - многие (стримы)
        original_method = handler.unary_unary

        # тут мы просто делаем обертку над нашим "роутом", делая ему дополнительный функционал, подобие декоратора, либо мидлвара,
        # просто через трай ексепты выбрасываем ошибки из роутов и через context.abort выдаем ошибку в респонс, а там уже в приложении FastApi мы ее обрабатываем
        async def wrapper(request, context: grpc.aio.ServicerContext):
            try:
                return await original_method(request, context)
            
            except InvalidCredentialsError as e:
                await context.abort(grpc.StatusCode.UNAUTHENTICATED, str(e))

            except ExpiredSignatureError:
                error_message = "Токен протух"
                await context.abort(grpc.StatusCode.UNAUTHENTICATED, error_message)

            except InvalidTokenError:
                error_message = "Недействительный токен"
                await context.abort(grpc.StatusCode.UNAUTHENTICATED, error_message)

            except InvalidOldPasswordError as e:
                await context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
                
            except UserNotFoundError as e:
                await context.abort(grpc.StatusCode.NOT_FOUND, str(e))

            except ValidationError as e:
                await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

            except IntegrityError:
                error_message = "Пользователь с такими данными уже существует"
                await context.abort(grpc.StatusCode.ALREADY_EXISTS, error_message)

            except Exception as e:  # noqa: BLE001
                error_message = "Внутренняя ошибка сервера"
                await context.abort(grpc.StatusCode.INTERNAL, str(e))

        # тут мы возвращаем в RPC тот же самый метод, который получили, только с обработкой ошибок, в целом ничего не меняем и передаем обратно реквесты и респонсы,
        # но т.к вся работа идет бинарно, то тут передаем для восстановления данных для работы с ними
        return grpc.unary_unary_rpc_method_handler(
            wrapper, request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer
        )