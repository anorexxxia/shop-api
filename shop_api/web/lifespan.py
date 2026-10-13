from contextlib import asynccontextmanager

import grpc
from config import config
from datasource.storage.storage import storage
from fastapi import FastAPI
from web.clients.auth_client import AuthClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await storage.delete_tables()
    # открываем канал для общения между приложениями
    channel = grpc.aio.insecure_channel(f"{config.auth.host}:{config.auth.port}")
    app.state.auth_client = AuthClient(channel)
    if config.main_instance:
        await storage.create_tables()
    yield
    await channel.close()
    await storage.async_engine.dispose()