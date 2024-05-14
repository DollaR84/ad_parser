import asyncio

from config import Config

from farfetch import FarfetchParser

from shop import ProductService


async def main():
    config = Config()
    parser = FarfetchParser(config)
    products = await parser.run()
    service = ProductService(config)
    service.load_products(products)


if "__main__" == __name__:
    asyncio.run(main())
