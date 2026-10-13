from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class RequestProduct(BaseModel):
    name: str = Field(min_length=2, max_length=50, examples=["Название"])
    category: str = Field(min_length=2, max_length=50, examples=["Категория"])
    price: Decimal = Field(gt=0, examples=[99.99])
    available_stock: int = Field(ge=0)
    supplier_id: int


class ResponseProduct(RequestProduct):
    id: int
    image_id: UUID | None