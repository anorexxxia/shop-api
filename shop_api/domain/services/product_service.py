from datasource.repositories import ProductRepository
from web.models import RequestProduct


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository


    async def get_all(self):
        return await self.repository.get_all()


    async def get_product(self, id):
        return await self.repository.get_product(id)

    
    async def add_a_product(self, product: RequestProduct):
        await self.repository.add_a_product(product)


    async def delete_a_product(self, id):
        await self.repository.delete_a_product(id)


    async def reducing_the_quantity_of_goods(self, id, amount):
        await self.repository.reducing_the_quantity_of_goods(id, amount)