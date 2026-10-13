from domain.services import SupplierService
from fastapi import APIRouter, Depends, Path, status
from web.dependencies import get_supplier_service
from web.exceptions import ValidationErrorResponse
from web.middleware import ProtectedRoute
from web.models import RequestAddress, RequestSupplier, ResponseSupplier

supplier_router = APIRouter(tags=["Supplier"], route_class=ProtectedRoute)


@supplier_router.get(
    "/suppliers",
    summary="Получить список всех поставщиков",
    response_description="Список поставщиков",
    response_model=list[ResponseSupplier],
)
async def get_suppliers(service: SupplierService = Depends(get_supplier_service)):  # noqa: B008
    return await service.get_suppliers()


@supplier_router.get(
    "/suppliers/{id}",
    summary="Получить поставщика по его id",
    response_description="Поставщик",
    response_model=ResponseSupplier,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
        status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def get_supplier(id: int = Path(ge=1), service: SupplierService = Depends(get_supplier_service)):  # noqa: B008
    return await service.get_supplier(id)


@supplier_router.post(
    "/suppliers",
    summary="Создать нового поставщика",
    response_description="Ответ об успешном создании",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
        status.HTTP_201_CREATED: {"content": {"application/json": {"example": {"message": "Поставщик успешно добавлен"}}}}
    }
)
async def create_supplier(supplier: RequestSupplier, service: SupplierService = Depends(get_supplier_service)):  # noqa: B008
    await service.add_a_supplier(supplier)
    return {"message": "Поставщик успешно добавлен"}


@supplier_router.delete(
    "/suppliers/{id}",
    summary="Удаление поставщика",
    response_description="Ответ об успешном удалении поставщика",
    responses={
        status.HTTP_200_OK: {"content": {"application/json": {"example": {"message": "Поставщик успешно удален"}}}},
        status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
        status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def delete_a_supplier(id: int = Path(ge=1), service: SupplierService = Depends(get_supplier_service)):  # noqa: B008
    await service.delete_a_supplier(id)
    return {"message": "Поставщик успешно удален"}


@supplier_router.patch(
    "/supplier/{id}",
    summary="Изменение адреса у поставщика",
    response_description="Ответ об успешном изменении адреса",
    responses={
        status.HTTP_200_OK: {"content": {"application/json": {"example": {"message": "Адрес успешно изменен"}}}},
        status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
        status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"}
    }
)
async def change_the_address(address: RequestAddress, id: int = Path(ge=1), service: SupplierService = Depends(get_supplier_service)):  # noqa: B008
    await service.change_the_address(id, address)
    return {"message": "Адрес успешно изменен"}