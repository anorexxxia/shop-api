# from datasource.mappers.client_mapper import client_to_orm
from datasource.exeptions.exeptions import NotFoundException
from datasource.models import ClientOrm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from web.models import RequestAddress, RequestClient


class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all(self, name, username, limit, ofset):
        query = select(ClientOrm).options(selectinload(ClientOrm.address))
        if name:
            query = query.filter(ClientOrm.client_name == name)
        if username:
            query = query.filter(ClientOrm.client_surname == username)
        if limit is not None:
            query = query.limit(limit)
        if ofset is not None:
            query = query.offset(ofset)
        
        result = (await self.session.execute(query)).scalars().all()
        return result


    async def add_a_client(self, client: RequestClient):
        # new_client = client_to_orm(client)
        new_client = client.client_to_orm()
        self.session.add(new_client)
        await self.session.commit()


    async def delete_a_client(self, id):
        client = await self.session.get(ClientOrm, id)
        if not client:
            raise NotFoundException(f"Клиента по id {id} не существует")
        # result = await self.session.execute(delete(ClientOrm).where(ClientOrm.id == id))
        # if result.rowcount == 0:
        #     raise Exception(f"Клиента по id {id} не существует")
        await self.session.delete(client)
        await self.session.commit()


    async def change_the_address(self, id, address: RequestAddress):
        client = await self.session.get(ClientOrm, id, options=[selectinload(ClientOrm.address)])
        if not client:
            raise NotFoundException(f"Клиента по id {id} не существует")

        client.address.country = address.country
        client.address.city = address.city
        client.address.street = address.street

        await self.session.commit()

