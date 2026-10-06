"""Validation d'un DataFrame complet (batch) avec pandera."""
import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series

from .constants import COUNTRIES, EMAIL_PATTERN, MAX_QUANTITY, STATUSES


class OrderSchema(pa.DataFrameModel):
    order_id: Series[int] = pa.Field(gt=0, unique=True)
    customer_email: Series[str] = pa.Field(str_matches=EMAIL_PATTERN)
    order_date: Series[pd.Timestamp]
    country: Series[str] = pa.Field(isin=COUNTRIES)
    quantity: Series[int] = pa.Field(ge=1, le=MAX_QUANTITY)
    unit_price: Series[float] = pa.Field(gt=0)
    total_amount: Series[float] = pa.Field(ge=0)
    status: Series[str] = pa.Field(isin=STATUSES)

    @pa.check("order_date", error="order_date est dans le futur")
    def not_in_future(cls, dates: Series[pd.Timestamp]) -> Series[bool]:
        return dates <= pd.Timestamp.now()

    @pa.dataframe_check(error="total_amount != quantity * unit_price")
    def total_is_consistent(cls, df: pd.DataFrame) -> Series[bool]:
        return (df["quantity"] * df["unit_price"] - df["total_amount"]).abs() < 0.01

    class Config:
        strict = True  # refuse les colonnes inattendues
        coerce = True  # convertit les types quand c'est possible
