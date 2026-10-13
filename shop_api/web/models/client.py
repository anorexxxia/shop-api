from datetime import date, datetime

from datasource.models import AddressOrm, ClientOrm
from enums import EnumGender
from pydantic import BaseModel, ConfigDict, Field
from web.models import RequestAddress


class RequestClient(BaseModel):
    client_name: str = Field(min_length=2, max_length=50, examples=["Имя1"])
    client_surname: str = Field(min_length=2, max_length=50, examples=["Фамилия1"])
    birthday: date
    gender: EnumGender
    registration_date: datetime
    address: RequestAddress

    def client_to_orm(self) -> ClientOrm:
        new_address = AddressOrm(**self.address.model_dump())
        new_client = ClientOrm(
        client_name=self.client_name,
        client_surname=self.client_surname,
        birthday=self.birthday,
        gender=self.gender,
        address=new_address
        )
        return new_client


class ResponseClient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_name: str = Field(examples=["Имя"])
    client_surname: str = Field(examples=["Фамилия"])
    birthday: date
    gender: EnumGender
    registration_date: datetime
    address: RequestAddress