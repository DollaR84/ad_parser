from typing import Literal

from pydantic import BaseModel


class Price(BaseModel):
    value: float
    currency: str


class Product(BaseModel):
    id: str
    offerId: str
    item_group_id: str
    mpn: str
    gtin: str | None = None

    title: str
    description: str | None = None

    image_link: str
    additionalImageLinks: list[str] | None = None

    link: str
    gender: str
    age_group: str | None = None

    brand: str
    color: str | None = None
    sizes: list[str] | None = None
    availability: Literal["in_stock", "out_of_stock", "preorder", "backorder"]
    price: Price

    condition: str | None = None
    channel: str
    contentLanguage: str
    targetCountry: str

    productTypes: list[str]
    google_product_category: str
