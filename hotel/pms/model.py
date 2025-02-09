import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


# --- Unified Model ---
class UpsellProduct(BaseModel):
    id: str = ""
    name: str = ""
    code: str = ""
    description: str = ""
    price: str = ""
    age_category: str = ""


# --- Adapter Base Class ---
class UpsellProductAdapter:
    """
    Base adapter interface for converting PMS provider data into the unified UpsellProduct model.
    """
    def __init__(self, raw_data: dict) -> None:
        self.raw_data = raw_data

    def convert(self) -> UpsellProduct:
        raise NotImplementedError("Subclasses must implement this method")