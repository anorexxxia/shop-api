from pydantic import BaseModel, ConfigDict, Field


class RequestAddress(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    country: str = Field(max_length=50, examples=["Страна1"])
    city: str = Field(max_length=100, examples=["Город1"])
    street: str = Field(max_length=100, examples=["Улица1"])