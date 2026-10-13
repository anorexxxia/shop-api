from fastapi import APIRouter

from .auth import auth_router
from .client import clients_router
from .image import image_router
from .product import product_router
from .supplier import supplier_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(clients_router)
api_router.include_router(product_router)
api_router.include_router(supplier_router)
api_router.include_router(image_router)
api_router.include_router(auth_router)