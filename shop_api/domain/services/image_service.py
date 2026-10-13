from datasource.repositories import ImagesRepository


class ImageService:
    def __init__(self, repository: ImagesRepository):
        self.repository = repository

    async def add_a_image(self, product_id, image_bytes):
        await self.repository.add_a_image(product_id, image_bytes)

    async def changing_the_image(self, id, image_bytes):
        await self.repository.changing_the_image(id, image_bytes)

    async def delete_a_image(self, id):
        await self.repository.delete_a_image(id)

    async def get_image(self, id):
        return await self.repository.get_image(id)

    async def get_image_of_the_product(self, product_id):
        return await self.repository.get_image_of_the_product(product_id)