from domain.services import ProductService
from fastapi import APIRouter, Depends, Path, Query, status
from web.dependencies import get_product_service
from web.exceptions import ValidationErrorResponse
from web.middleware import ProtectedRoute
from web.models import RequestProduct, ResponseProduct

product_router = APIRouter(tags=["products"], route_class=ProtectedRoute)

@product_router.get(
    "/products",
    summary="Получение всех доступных товаров",
    response_description="Успешное получение списка товаров",
    response_model=list[ResponseProduct]
)
async def get_products(service: ProductService = Depends(get_product_service)):  # noqa: B008
    return await service.get_all()


@product_router.get(
    "/products/{id}",
    summary="Получение товара по его id",
    response_description="Успешное получение товара",
    response_model=ResponseProduct,
    responses={
    status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
    status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def get_product(id: int = Path(ge=1), service: ProductService = Depends(get_product_service)):  # noqa: B008
    return await service.get_product(id)


@product_router.post(
    "/products",
    summary="Добавить новый товар", 
    response_description="Товар успешно добавлен",
    status_code=status.HTTP_201_CREATED,
    responses={
    status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
    status.HTTP_201_CREATED: {"content": {"application/json": {"example": {"message": "Товар успешно добавлен"}}}},
    status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def add_a_product(new_product: RequestProduct, service: ProductService = Depends(get_product_service)):  # noqa: B008
    await service.add_a_product(new_product)
    return {"message": "Товар успешно добавлен"}


@product_router.patch(
    "/products/{id}",
    summary="Уменьшение количества товара",
    response_description="Успешно",
    responses={
    status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
    status.HTTP_200_OK: {"content": {"application/json": {"example": {"message": "Уменьшение количества товара на N ед."}}}},
    status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def reducing_the_quantity_of_goods(
    id: int = Path(ge=1), amount: int = Query(ge=1), 
    service: ProductService = Depends(get_product_service)  # noqa: B008
    ):
    await service.reducing_the_quantity_of_goods(id, amount)
    return {"message": f"Уменьшение количества товара на {amount} ед."}


@product_router.delete(
    "/products/{id}",
    summary="Удаление товара",
    response_description="Товар успешно удален",
    responses={
    status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
    status.HTTP_200_OK: {"content": {"application/json": {"example": {"message": "Товар по id N успешно удален"}}}},
    status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def delete_a_product(id: int = Path(ge=1), service: ProductService = Depends(get_product_service)):  # noqa: B008
    await service.delete_a_product(id)
    return {"message": f"Товар по id {id} успешно удален"}