import pytest_asyncio
from config import config
from datasource.models import Base
from datasource.storage.storage import storage
from httpx import ASGITransport, AsyncClient
from main import app
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{config.db.db_user}:{config.db.db_password}"
    f"@localhost/test_shop_api"
)


@pytest_asyncio.fixture
async def client():
    test_engine = create_async_engine(TEST_DATABASE_URL)

    test_session_factory = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session_factory() as session:

        async def override_get_session():
            yield session

        app.dependency_overrides[
            storage.get_async_session
        ] = override_get_session

        transport = ASGITransport(app=app, raise_app_exceptions=False)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            yield client

        app.dependency_overrides.clear()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()