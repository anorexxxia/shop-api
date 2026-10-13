from contextlib import asynccontextmanager

from datasource.models.user import Base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Storage:
    def __init__(self, db_url) -> None:
        self.db_url = db_url
        self.async_engine = create_async_engine(self.db_url, echo=False)
        self._async_session_factory = async_sessionmaker(bind=self.async_engine, expire_on_commit=False)


    @asynccontextmanager
    async def session(self):
        async with self._async_session_factory() as session:
            yield session


    async def create_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


    async def delete_table(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)