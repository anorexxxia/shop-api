import asyncio

from di.container import container
from gRPC.grpc_server import serve


async def main():
    await container.storage.create_tables()
    await serve()

if __name__ == "__main__":
    asyncio.run(main())