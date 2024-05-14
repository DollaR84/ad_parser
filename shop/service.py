import json
import logging

from config import Config

from schemas import Product

from .client import Client


class ProductService:

    def __init__(self, config: Config):
        self.cfg = config
        self.client = Client(self.cfg).get()
        self.logger = logging.getLogger()

    def batch_products(self, products: list[Product]) -> list[Product]:
        for i in range(0, len(products), self.cfg.batch_size):
            yield products[i:i + self.cfg.batch_size]

    def load_products(self, products: list[Product]):
        for items in self.batch_products(products):
            batch = {
                "entries": [{
                    "batchId": i,
                    "merchantId": self.cfg.merchant_id,
                    "method": "insert",
                    "product": product.dict(exclude_unset=True),
                } for i, product in enumerate(items)]
            }

            request = self.client.products().custombatch(body=batch)
            result = request.execute()

            if result["kind"] == "content#productsCustomBatchResponse":
                entries = result["entries"]
                for entry in entries:
                    product = entry.get("product")
                    errors = entry.get("errors")
                    if product:
                        product_id = product["id"]
                        self.logger.debug(f"Product '{product_id}' was created.")
                    elif errors:
                        batch_id = entry["batchId"]
                        self.logger.error(f"Errors for batch entry {batch_id}:")
                        self.logger.error(json.dumps(
                            errors, sort_keys=True, indent=2,
                            separators=(",", ": ")
                        ))

            else:
                self.logger.error(f"There was an error. Response: {result}")
