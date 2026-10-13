from datasource.exeptions.exeptions import NotFoundException
from datasource.mappers.product_mapper import to_orm
from datasource.models import ProductOrm, SupplierOrm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from web.models import RequestProduct


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    def _check_product(self, product, id):
        if not product:
            raise NotFoundException(f"Продукта по id {id} не существует")


    async def get_all(self):
        query = select(ProductOrm).where(ProductOrm.available_stock > 0)
        result = (await self.session.execute(query)).scalars().all()
        return result


    async def get_product(self, id):
        product = await self.session.get(ProductOrm, id)
        self._check_product(product, id)
        return product

    
    async def add_a_product(self, product: RequestProduct):
        supplier = await self.session.get(SupplierOrm, product.supplier_id)
        if not supplier:
            raise NotFoundException(f"Поставщика по id {product.supplier_id} не существует")
        
        new_product = to_orm(product)
        self.session.add(new_product)
        await self.session.commit()


    async def delete_a_product(self, id):
        product = await self.session.get(ProductOrm, id)
        self._check_product(product, id)

        await self.session.delete(product)
        await self.session.commit()


    async def reducing_the_quantity_of_goods(self, id, amount):
        product = await self.session.get(ProductOrm, id)
        self._check_product(product, id)
        count = product.available_stock - amount

        if count < 0:
            raise Exception(f"остаток продукта {product.available_stock}, уменьшать не больше, чем остаток")  # noqa: TRY002

        product.available_stock -= amount
        await self.session.commit()