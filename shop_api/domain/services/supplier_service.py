from datasource.repositories import SupplierRepository


class SupplierService:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository


    async def get_suppliers(self):
        return await self.repository.get_all()


    async def get_supplier(self, id):
        return await self.repository.get_supplier(id)


    async def add_a_supplier(self, supplier):
        await self.repository.add_a_supplier(supplier)


    async def change_the_address(self, id, address):
        await self.repository.change_the_address(id, address)


    async def delete_a_supplier(self, id):
        await self.repository.delete_a_supplier(id)