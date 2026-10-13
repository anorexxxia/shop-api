from typing import Any

import grpc
from datasource.exeptions.exeptions import NotFoundException
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError


class ValidationErrorResponse(BaseModel):
    message: str = Field(examples=["Неверные данные"])
    errors: list[dict[str, Any]] = Field(examples=[[{"type": "тип ошибки", "loc": "место ошибки", "msg": "расшифровка"}]])


async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Неверные данные", "errors": exc.errors()})


async def integrity_exception_handler(request, exc: IntegrityError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Ошибка добавления в БД", "errors": str(exc.orig)})


async def not_found_exception(request, exc: NotFoundException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"errors": str(exc)})


async def grpc_exception_handler(request, exc: grpc.aio.AioRpcError):
    errors = exc.code()
    content = {"errors": exc.details()}
    match errors:
        case grpc.StatusCode.ALREADY_EXISTS:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=content)
        case grpc.StatusCode.INVALID_ARGUMENT:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
        case grpc.StatusCode.UNAUTHENTICATED:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=content)
        case grpc.StatusCode.NOT_FOUND:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content)
        case grpc.StatusCode.PERMISSION_DENIED:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=content)
        case _:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content)


async def any_exception_handler(request, exc: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Ошибка", "errors": str(exc)})


def packaging_errors(app: FastAPI):
    errors = [
    (RequestValidationError, validation_exception_handler),
    (IntegrityError, integrity_exception_handler),
    (NotFoundException, not_found_exception),
    (grpc.aio.AioRpcError, grpc_exception_handler),
    (Exception, any_exception_handler)
    ]
    for er, f in errors:
        app.add_exception_handler(er, f)