from dataclasses import dataclass
import os


@dataclass
class Config:
    default_sleep_timeout: float = 0.5
    language: str = "en"
    country: str = "ua"

    merchant_id: int = int(os.getenv("MERCHANT_ID"))
    merchant_name: str = os.getenv("MERCHANT_NAME")
    creds_file_path: str = os.getenv("CREDS_FILE_PATH")
    service_name: str = "content"
    service_version: str = "v2.1"
    batch_size: int = 25
    channel: str = "online"

    @property
    def application_name(self):
        return f"Content API for Shopping {self.merchant_name}"

    @property
    def scope(self):
        return f"https://www.googleapis.com/auth/{self.service_name}"
