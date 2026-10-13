from collections.abc import AsyncGenerator

from config import config
from datasource.models import Base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Storage:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.async_engine = create_async_engine(db_url, echo=False)
        self._async_session_factory = async_sessionmaker(bind=self.async_engine, expire_on_commit=False)
        # Base.metadata.drop_all(self.engine)
        # Base.metadata.create_all(self.engine)


    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._async_session_factory() as session:
            yield session

    async def create_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def delete_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

storage = Storage(config.db.SQLALCHEMY_DATABASE_URI)