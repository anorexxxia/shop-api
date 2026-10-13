from uuid import UUID

from domain.services import ImageService
from fastapi import APIRouter, Depends, Path, Query, Response, UploadFile, status
from web.dependencies import get_image_service
from web.exceptions import ValidationErrorResponse
from web.middleware import ProtectedRoute

image_router = APIRouter(tags=["Images"], route_class=ProtectedRoute)


@image_router.post(
    "/images",
    summary="Загрузка изображения по id товара",
    response_description="Изображениe загружено",
    status_code=status.HTTP_201_CREATED,
    responses={
    status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
    status.HTTP_201_CREATED: {"content": {"application/json": {"example": {"message": "Изображение успешно добавлено"}}}}
    }
)
async def add_a_image(file: UploadFile, product_id: int = Query(ge=1), service: ImageService = Depends(get_image_service)):  # noqa: B008
    image_bytes = await file.read()
    await service.add_a_image(product_id, image_bytes)
    return {"message": f"Изображение успешно добавлено к товару с id {product_id}"}


@image_router.put(
    "/images/{id}",
    summary="Изменение изображения",
    response_description="Изображение изменено",
    responses={
    status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
    status.HTTP_200_OK: {"content": {"application/json": {"example": {"message": "Изображение изменено"}}}},
    status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def changing_the_image(file: UploadFile, id: UUID, service: ImageService = Depends(get_image_service)):  # noqa: B008
    image_bytes = await file.read()
    await service.changing_the_image(id, image_bytes)
    return {"message": "Изображение изменено"}


@image_router.delete(
    "/images/{id}",
    summary="Удаление изображения",
    response_description="Изображение удалено",
    responses={
    status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
    status.HTTP_200_OK: {"content": {"application/json": {"example": {"message": "Изображение удалено"}}}},
    status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def delete_a_image(id: UUID, service: ImageService = Depends(get_image_service)):  # noqa: B008
    await service.delete_a_image(id)
    return {"message": "Изображение удалено"}


@image_router.get(
    "/images/",
    summary="Получение изображения по id изображения",
    response_description="Получено изображение",
    responses={
    status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
    status.HTTP_200_OK: {"content": {"application/json": {"example": {"message": "Изображение"}}}},
    status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def get_image(id: UUID, service: ImageService = Depends(get_image_service)):  # noqa: B008
    image_bytes = await service.get_image(id)
    return Response(content=image_bytes, media_type="application/octet-stream", 
                    headers={"Content-Disposition": f'attachment; filename="image_{id}.jpg"'})


@image_router.get(
    "/product/{product_id}/image",
    summary="Получение изображения по id товара",
    response_description="Получено изображение",
    responses={
    status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
    status.HTTP_200_OK: {"content": {"application/json": {"example": {"message": "Изображение"}}}},
    status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def get_image_of_the_product(product_id: int = Path(ge=1), service: ImageService = Depends(get_image_service)):  # noqa: B008
    image_bytes = await service.get_image_of_the_product(product_id)
    return Response(content=image_bytes, media_type="application/octet-stream", 
                    headers={"Content-Disposition": f'attachment; filename="image_{product_id}.jpg"'})