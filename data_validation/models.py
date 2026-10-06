"""Validation d'un enregistrement unique (ex. payload d'API) avec pydantic."""
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field, FilePath, field_validator, model_validator

from .constants import EMAIL_PATTERN, MAX_QUANTITY, Country, Status


class Order(BaseModel):
    order_id: int = Field(gt=0)
    customer_email: str = Field(pattern=EMAIL_PATTERN)
    order_date: datetime
    country: Country
    quantity: int = Field(ge=1, le=MAX_QUANTITY)
    unit_price: float = Field(gt=0)
    total_amount: float = Field(ge=0)
    status: Status

    @field_validator("order_date")
    @classmethod
    def not_in_future(cls, value: datetime) -> datetime:
        if value.replace(tzinfo=None) > datetime.now():
            raise ValueError("order_date est dans le futur")
        return value

    @model_validator(mode="after")
    def total_is_consistent(self) -> "Order":
        if abs(self.quantity * self.unit_price - self.total_amount) >= 0.01:
            raise ValueError("total_amount != quantity * unit_price")
        return self


class ValidationConfig(BaseModel):
    """Paramètres du script : pydantic vérifie que le fichier d'entrée existe."""

    input_path: FilePath
    output_dir: Path = Path("output")
