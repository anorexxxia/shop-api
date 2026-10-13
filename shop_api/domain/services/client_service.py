from datasource.repositories import ClientRepository
from web.models import RequestClient


class ClientService:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    async def get_all(self, name, username, limit, ofset):
        return await self.repository.get_all(name, username, limit, ofset)

    async def add_a_client(self, client: RequestClient):
        await self.repository.add_a_client(client)

    async def delete_a_client(self, id):
        await self.repository.delete_a_client(id)

    async def change_the_address(self, id, address):
        await self.repository.change_the_address(id, address)