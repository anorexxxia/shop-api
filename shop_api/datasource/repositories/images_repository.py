from datasource.exeptions.exeptions import NotFoundException
from datasource.models import ImagesOrm, ProductOrm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class ImagesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    def _check_product(self, product_id, product):
        if not product:
            raise NotFoundException(f"Нет товара с таким id {product_id}")


    def _check_image(self, image):
        if not image:
            raise NotFoundException("Нет картинки с таким id")

        
    async def add_a_image(self, product_id, image_bytes):
        product = await self.session.get(ProductOrm, product_id)
        self._check_product(product_id, product)
        image = ImagesOrm(image_bytes)
        self.session.add(image)
        await self.session.flush()

        if product.image_id:
            await self.delete_a_image(product.image_id)

        product.image_id = image.id
        await self.session.commit()


    async def changing_the_image(self, id, image_bytes):
        image = await self.session.get(ImagesOrm, id)
        self._check_image(image)
        image.image = image_bytes
        await self.session.commit()


    async def delete_a_image(self, id):
        image = await self.session.get(ImagesOrm, id)
        self._check_image(image)
        await self.session.delete(image)
        await self.session.commit()


    async def get_image(self, id):
        image = await self.session.get(ImagesOrm, id)
        self._check_image(image)
        return image.image


    async def get_image_of_the_product(self, product_id):
        product = await self.session.get(ProductOrm, product_id, options=[selectinload(ProductOrm.image)])
        self._check_product(product_id, product)
        return product.image.image


