from datasource.exeptions.exeptions import NotFoundException
from datasource.mappers.supplier_mapper import supplier_to_orm
from datasource.models import SupplierOrm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from web.models import RequestAddress, RequestSupplier


class SupplierRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    def _check_supplier(self, id, supplier):
        if not supplier:
            raise NotFoundException(f"Поставщика по id {id} не существует")


    async def get_all(self):
        query = select(SupplierOrm).options(selectinload(SupplierOrm.address))
        result = (await self.session.execute(query)).scalars().all()
        return result


    async def get_supplier(self, id):
        supplier =  await self.session.get(SupplierOrm, id, options=[selectinload(SupplierOrm.address)])
        self._check_supplier(id, supplier)

        return supplier


    async def add_a_supplier(self, supplier: RequestSupplier):
        new_supplier = supplier_to_orm(supplier)
        self.session.add(new_supplier)
        await self.session.commit()


    async def change_the_address(self, id, address: RequestAddress):
        supplier = await self.session.get(SupplierOrm, id, options=[selectinload(SupplierOrm.address)])
        self._check_supplier(id, supplier)

        supplier.address.country = address.country
        supplier.address.city = address.city
        supplier.address.street = address.street

        await self.session.commit()


    async def delete_a_supplier(self, id):
        # result = await self.session.execute(delete(SupplierOrm).where(SupplierOrm.id == id))
        suplier = await self.session.get(SupplierOrm, id)
        if not suplier:
            raise NotFoundException(f"Клиента по id {id} не существует")
        
        # if result.rowcount == 0:
        #     raise Exception(f"Клиента по id {id} не существует")
        await self.session.delete(suplier)
        await self.session.commit()