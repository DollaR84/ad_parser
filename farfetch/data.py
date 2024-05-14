class FarfetchData:

    def __init__(self):
        self.url = "https://www.farfetch.com/ca/shopping/women/dresses-1/items.aspx"
        self.api_url = "https://www.farfetch.com/ca/plpslice/listing-api/products-facets"

        self.view: int = 60
        self.pagetype: str = "Shopping"
        self.rootCategory: str = "Women"
        self.pricetype: str = "FullPrice"
        self.category: str = "135979"

        self.pages = self.page_gen()

    def page_gen(self) -> int:
        for page_id in range(1, 3):
            yield page_id

    def get_params(self, page_id: int) -> str:
        return {
            "page": page_id,
            "view": self.view,
            "pagetype": self.pagetype,
            "rootCategory": self.rootCategory,
            "pricetype": self.pricetype,
            "c-category": self.category,
        }

    @property
    def params(self) -> list:
        return [self.get_params(page_id) for page_id in self.pages]
