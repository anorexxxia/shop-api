from dataclasses import dataclass, field

from environs import Env


@dataclass
class DatabaseConfig:
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    SQLALCHEMY_DATABASE_URI: str = field(init=False)
    

    def __post_init__(self):
        self.SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


@dataclass
class Config:
    db: DatabaseConfig
    SECRET_KEY: str

def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        db=DatabaseConfig(
            db_user=env('DB_USER'), 
            db_password=env('DB_PASSWORD'), 
            db_host=env('DB_HOST'),
            db_port=env('DB_PORT'), 
            db_name=env('DB_NAME')
        ),
        SECRET_KEY=env('SECRET_KEY')
    )