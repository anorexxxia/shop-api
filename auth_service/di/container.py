from config import load_config
from datasource.repositories.postgres_user_repository import UserRepository
from datasource.storage import Storage
from domain.security import JWTService, PasswordHasher
from domain.services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession


class Container:
    def __init__(self) -> None:
        self.config = load_config()
        self.storage = Storage(self.config.db.SQLALCHEMY_DATABASE_URI)
        self.password_hasher = PasswordHasher()
        self.jwt_service = JWTService(secret_key=self.config.SECRET_KEY, lifetime=15)


    def create_auth_service(self, session: AsyncSession) -> AuthService:
        repository = UserRepository(session)

        return AuthService(repository, self.password_hasher, self.jwt_service)

container = Container()