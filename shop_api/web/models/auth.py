from pydantic import BaseModel, EmailStr, Field, model_validator
from pydantic_core import PydanticCustomError
from pydantic_extra_types.phone_numbers import PhoneNumber


class RequestUser(BaseModel):
    firstname: str = Field(min_length=2, max_length=50)
    lastname: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone: PhoneNumber = Field(examples=["+79991234567"])
    password: str = Field(min_length=4, max_length=256)


class UserLogin(BaseModel):
    login: EmailStr
    password: str = Field(min_length=4, max_length=256)


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=4, max_length=256)
    new_password: str = Field(min_length=4, max_length=256)


    @model_validator(mode="after")
    def validate_password(self) -> "ChangePasswordRequest":
        if self.old_password == self.new_password:
            raise PydanticCustomError("same_password", "Новый пароль не должен совпадать со старым")
        
        return self