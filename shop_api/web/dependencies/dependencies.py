from typing import Annotated

from datasource.repositories import (
    ClientRepository,
    ImagesRepository,
    ProductRepository,
    SupplierRepository,
)
from datasource.storage.storage import storage
from domain.services import ClientService, ImageService, ProductService, SupplierService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

DBSession = Annotated[AsyncSession, Depends(storage.get_async_session)]


# зависимости для продукта
def get_product_repository(session: DBSession) -> ProductRepository:
    return ProductRepository(session)

def get_product_service(repository: Annotated[ProductRepository, Depends(get_product_repository)]) -> ProductService:
    return ProductService(repository)


# зависимости для клиентов
def get_client_repository(session: DBSession) -> ClientRepository:
    return ClientRepository(session)

def get_client_service(repository: Annotated[ClientRepository, Depends(get_client_repository)]) -> ClientService:
    return ClientService(repository)


# зависимости для поставщиков
def get_supplier_repository(session: DBSession) -> SupplierRepository:
    return SupplierRepository(session)

def get_supplier_service(repository: Annotated[SupplierRepository, Depends(get_supplier_repository)]) -> SupplierService:
    return SupplierService(repository)


# зависимости для картинок
def get_image_repository(session: DBSession) -> ImagesRepository:
    return ImagesRepository(session)

def get_image_service(repository: Annotated[ImagesRepository, Depends(get_image_repository)]) -> ImageService:
    return ImageService(repository)