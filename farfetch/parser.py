import asyncio
import logging
import random

from aiohttp import ClientSession

from bs4 import BeautifulSoup

from config import Config

from fake_useragent import UserAgent

from .data import FarfetchData

from schemas import Price, Product


class FarfetchParser:

    def __init__(self, config: Config):
        self.cfg = config
        self.data = FarfetchData()
        self.ua = UserAgent()

        self.results: list[Product] = []
        random.seed()

    @property
    def headers(self) -> dict:
        return {
            "Origin": "https://www.farfetch.com",
            "Referer": "https://www.farfetch.com/ca/shopping/women/dresses-1/items.aspx",
            "User-Agent": self.ua.chrome,
        }

    async def sleep(self):
        timeout = random.random() + self.cfg.default_sleep_timeout
        await asyncio.sleep(timeout)

    async def run(self) -> list[Product]:
        await self.parse()
        return self.results

    async def parse(self):
        async with ClientSession(headers=self.headers) as session:
            try:
                data = ""
                async with session.get(self.data.url) as response:
                    data = await response.text()
                product_type = self.process_Breadcrumbs(data)
                await self.sleep()

                for params in self.data.params:
                    async with session.get(self.data.api_url, params=params) as response:
                        data = await response.json()
                        self.process_data(data, product_type)
                        await self.sleep()
            except Exception as err:
                logging.error(err, exc_info=True)

    def process_Breadcrumbs(self, data: str) -> str:
        bs = BeautifulSoup(data, "html.parser")
        Breadcrumbs = []
        for Breadcrumb in bs.find_all("a", {"data-component": "Breadcrumb"}):
            Breadcrumbs.append(Breadcrumb.find("span").text)
        last_Breadcrumb = bs.find("span", {"data-component": "Breadcrumb"})
        if last_Breadcrumb:
            Breadcrumbs.append(last_Breadcrumb.text)
        return " > ".join(Breadcrumbs)

    def process_data(self, data: dict, product_type: str):
        base_url = "https://www.farfetch.com"
        categories = product_type.split(" > ")

        for item in data.get("listingItems", {}).get("items", []):
            item_group_id = item.get("id")
            if not item_group_id:
                continue

            brand = item.get("brand", {}).get("name")
            short_description = item.get("shortDescription")
            images = item.get("images", {})
            price = item.get("priceInfo", {})

            for size in item.get("availableSizes", []):
                size = size.get("size")
                offer_id = f"{item_group_id}-{size}"

                product = Product(
                    id=offer_id,
                    offerId=offer_id,
                    item_group_id=str(item_group_id),
                    mpn=item.get("mpn", str(item_group_id)),
                    title=f"{brand}: {short_description}",
                    description=item.get("description", short_description),
                    brand=brand,
                    gender=item.get("gender"),
                    image_link=images.get("cutOut"),
                    additionalImageLinks=[images.get("model")],
                    price=Price(
                        value=price.get("finalPrice"),
                        currency=price.get("currencyCode"),
                    ),
                    gtin=item.get("gtin"),
                    age_group=item.get("age_group"),
                    color=item.get("color"),
                    link=base_url + item.get("url"),
                    sizes=[size],
                    availability="in_stock" if bool(item.get("stockTotal", 0)) else "out_of_stock",
                    condition=item.get("condition"),
                    channel=self.cfg.channel,
                    contentLanguage=self.cfg.language,
                    targetCountry=self.cfg.country,
                    productTypes=[product_type],
                    google_product_category=" > ".join([categories[1], categories[2]]),
                )
                self.results.append(product)
