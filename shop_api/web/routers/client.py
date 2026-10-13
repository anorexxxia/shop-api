from domain.services import ClientService
from fastapi import APIRouter, Depends, Path, Query, status
from web.dependencies import get_client_service
from web.exceptions import ValidationErrorResponse
from web.middleware import ProtectedRoute
from web.models import RequestAddress, RequestClient, ResponseClient

clients_router = APIRouter(tags=["Clients"], route_class=ProtectedRoute)


@clients_router.get(
    "/clients",
    summary="Получить список всех клиентов",
    description="Возвращает информацию о клиентах, можно указать Имя, Фамилию, лимит и офсет",
    response_description="Cписок всех клиентов",
    response_model=list[ResponseClient],
    responses={status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"}}
)
async def get_clients(
    name: str | None = Query(None, description="Имя клиента"), 
    lastname: str | None = Query(None, description="Фамилия клиента"),
    limit: int = Query(None, ge=0, description="Сколько максимум вывести"), 
    ofset: int | None = Query(None, ge=0, description="Сдвиг на определенное количество"), 
    service: ClientService = Depends(get_client_service)  # noqa: B008
    ):
    return await service.get_all(name, lastname, limit, ofset)


@clients_router.post(
    "/clients", 
    summary="Добавить нового клиента",
    description="Создает нового клиента",
    response_description="Ответ об успешном создании",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"},
        status.HTTP_201_CREATED: {"content": {"application/json": {"example": {"message": "Клиент успешно создан"}}}}
        }
)
async def create_client(client: RequestClient, service: ClientService = Depends(get_client_service)):  # noqa: B008
    await service.add_a_client(client)
    return {"message": "Клиент успешно создан"}


@clients_router.delete(
    "/clients/{id}",
    summary="Удаление клиента по его id", 
    response_description="Ответ об успешном удалении",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"},
        status.HTTP_200_OK: {"content": {"application/json": {"example": {"message": "Клиент успешно удален"}}}},
        status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"}
        }
)
async def delete_a_client(id: int = Path(ge=1), service: ClientService = Depends(get_client_service)):  # noqa: B008
    await service.delete_a_client(id)
    return {"message": "Клиент успешно удален"}


@clients_router.patch(
    "/clients/{id}",
    summary="Изменение адреса у клиента",
    response_description="Ответ об успешном изменении адреса",
    responses={
    status.HTTP_404_NOT_FOUND: {"description": "404_NOT_FOUND"},
    status.HTTP_200_OK: {"content": {"application/json": {"example": {"message": "Адрес успешно изменен"}}}},
    status.HTTP_400_BAD_REQUEST: {"model": ValidationErrorResponse, "description": "Ошибка валидации данных"}
    }
)
async def change_the_address(address: RequestAddress, id: int = Path(ge=1), service: ClientService = Depends(get_client_service)):  # noqa: B008
    await service.change_the_address(id, address)
    return {"message": "Адрес успешно изменен"}