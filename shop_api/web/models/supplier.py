from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from web.models import RequestAddress


class RequestSupplier(BaseModel):
    name: str = Field(max_length=100, examples=["Название"])
    phone_number: PhoneNumber = Field(examples=["+79991234567"])
    address: RequestAddress


class ResponseSupplier(RequestSupplier):
    model_config = ConfigDict(from_attributes=True)

    id: int