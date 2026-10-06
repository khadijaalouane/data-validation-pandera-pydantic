import pandas as pd
import pandera.pandas as pa
import pytest

from data_validation.schemas import OrderSchema
from data_validation.validate import split_valid_invalid


@pytest.fixture
def valid_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": [1, 2],
            "customer_email": ["a@example.com", "b@example.com"],
            "order_date": ["2025-01-10", "2025-02-11"],
            "country": ["MA", "FR"],
            "quantity": [2, 1],
            "unit_price": [10.0, 25.5],
            "total_amount": [20.0, 25.5],
            "status": ["pending", "shipped"],
        }
    )


def test_valid_dataframe_passes(valid_df):
    assert len(OrderSchema.validate(valid_df)) == 2


@pytest.mark.parametrize(
    "column, bad_value",
    [
        ("quantity", -1),
        ("customer_email", "pas-un-email"),
        ("country", "XX"),
        ("status", "unknown"),
        ("order_date", "2999-01-01"),
        ("unit_price", 0.0),
    ],
)
def test_invalid_value_is_rejected(valid_df, column, bad_value):
    valid_df.loc[0, column] = bad_value
    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(valid_df)


def test_duplicate_order_id_is_rejected(valid_df):
    valid_df.loc[1, "order_id"] = 1
    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(valid_df)


def test_inconsistent_total_is_rejected(valid_df):
    valid_df.loc[0, "total_amount"] = 999.0
    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(valid_df)


def test_unexpected_column_is_rejected(valid_df):
    valid_df["extra"] = 1
    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(valid_df)


def test_split_valid_invalid(valid_df):
    valid_df.loc[0, "quantity"] = -5
    valid, invalid, failures = split_valid_invalid(valid_df)
    assert len(valid) == 1
    assert len(invalid) == 1
    assert not failures.empty
