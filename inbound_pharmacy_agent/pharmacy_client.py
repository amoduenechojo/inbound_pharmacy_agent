import re
import requests
from typing import Optional
from models import Pharmacy

API_URL = "https://67e14fb758cc6bf785254550.mockapi.io/pharmacies"


def _digits(value: Optional[str]) -> str:
    return re.sub(r"\D", "", value or "")


class PharmacyClient:
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url

    def get_by_phone(self, phone: str) -> Optional[Pharmacy]:

        try:
            response = requests.get(self.base_url, timeout=20)
            response.raise_for_status()
            records = response.json()
        except requests.RequestException:
            return None

        target = _digits(phone)
        for record in records:
            if _digits(record.get("phone")) == target:
                return self._normalize(record)
        return None

    def _normalize(self, record: dict) -> Pharmacy:
        if "rxVolume" in record:
            rx_volume = record.get("rxVolume")
            location = record.get("address")
        else:
            prescriptions = record.get("prescriptions", [])
            total = sum(add.get("count", 0) for add in prescriptions)

            rx_volume = total or None
            city, state = record.get("city"), record.get("state")
            location = f"{city}, {state}" if city and state else (city or state)

        return Pharmacy(
            id=str(record.get("id")) if record.get("id") is not None else None,
            name=record.get("name", "Unknown Pharmacy"),
            phone=record.get("phone", ""),
            location=location,
            rx_volume=rx_volume,
            is_known=True
        )