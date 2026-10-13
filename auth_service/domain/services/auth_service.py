from domain.exceptions import (
    InvalidCredentialsError,
    InvalidOldPasswordError,
    UserNotFoundError,
)
from domain.interfaces import (
    PasswordHasherInterface,
    TokenServiseInterface,
    UserRepositoryInterface,
)
from domain.models import ChangePasswordModel, LoginModel, ResetPasswordModel, User
from domain.security import generate_password
from jwt import InvalidTokenError


class AuthService:
    def __init__(
        self, 
        repository: UserRepositoryInterface, 
        password_hasher: PasswordHasherInterface, 
        token_service: TokenServiseInterface
    ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.token_service = token_service


    async def register(self, new_user: User):
        password_hash = self.password_hasher.hash(new_user.password)
        user_with_hash = new_user.model_copy(update={"password": password_hash})
        user = await self.repository.create(user_with_hash)
        token = self.token_service.create_token(user)

        return token


    async def login(self, authorization: LoginModel):
        user = await self.repository.get_by_email(authorization.login)

        if user is None or not self.password_hasher.verify(authorization.password, user.password):
            raise InvalidCredentialsError()

        token = self.token_service.create_token(user)

        return token


    async def change_password(self, token: str, psw: ChangePasswordModel):
        payload = self.token_service.verify_token(token)
        user_id = payload.get('sub')

        if user_id is None:
            raise InvalidTokenError()
        
        user_id = int(user_id)
        
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(f"Пользователя с таким id: {user_id} не существует")

        if not self.password_hasher.verify(psw.old_password, user.password):
            raise InvalidOldPasswordError()

        password_hash = self.password_hasher.hash(psw.new_password)

        await self.repository.change_password(user_id, password_hash)

        token = self.token_service.create_token(user)

        return token


    async def reset_password(self, email: ResetPasswordModel):
        user = await self.repository.get_by_email(email.email)

        if user is None:
            raise UserNotFoundError(f"Нет пользователя с таким емайлом {email.email}")

        password = generate_password()
        password_hash = self.password_hasher.hash(password)
        await self.repository.change_password(user_id=user.id, password=password_hash)
        print(f"Новый пароль для {email.email}: {password}")