import logging
from decimal import Decimal, InvalidOperation
from typing import Annotated

from pydantic import BaseModel, Field, field_validator
from pydantic.v1 import validator

logger = logging.getLogger(__name__)


# --- Unified Model ---
class UpsellProduct(BaseModel):
    id: str
    name: str
    code: str
    description: str
    price: str
    age_category: str

    def must_not_be_empty(cls, v, field):
        logger.debug(f"Validating field '{field.name}' with value: {v!r}")
        if not v or not v.strip():
            raise ValueError(f"'{field.name}' must not be empty")
        return v


# --- Adapter Base Class ---
class UpsellProductAdapter:
    """
    Base adapter interface for converting PMS provider data into the unified UpsellProduct model.
    """
    def __init__(self, raw_data: dict) -> None:
        self.raw_data = raw_data

    def convert(self) -> UpsellProduct:
        raise NotImplementedError("Subclasses must implement this method")