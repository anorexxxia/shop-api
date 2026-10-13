from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from pydantic_core import PydanticCustomError
from pydantic_extra_types.phone_numbers import PhoneNumber


class User(BaseModel):
    firstname: str = Field(min_length=2, max_length=50)
    lastname: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone: PhoneNumber
    password: str = Field(min_length=4, max_length=256)


class UserResponse(User):
    id: int

    model_config = ConfigDict(from_attributes=True)


class LoginModel(BaseModel):
    login: EmailStr
    password: str = Field(min_length=4, max_length=256)


class LoginResponseModel(LoginModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ChangePasswordModel(BaseModel):
    old_password: str = Field(min_length=4, max_length=256)
    new_password: str = Field(min_length=4, max_length=256)


    @model_validator(mode="after")
    def validate_password(self) -> "ChangePasswordModel":
        if self.old_password == self.new_password:
            raise PydanticCustomError("same_password", "Новый пароль не должен совпадать со старым")
        
        return self

class ResetPasswordModel(BaseModel):
    email: EmailStr