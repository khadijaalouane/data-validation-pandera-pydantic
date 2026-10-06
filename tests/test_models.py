import pytest
from pydantic import ValidationError

from data_validation.models import Order


@pytest.fixture
def payload() -> dict:
    return {
        "order_id": 1,
        "customer_email": "a@example.com",
        "order_date": "2025-01-10",
        "country": "MA",
        "quantity": 2,
        "unit_price": 10.0,
        "total_amount": 20.0,
        "status": "pending",
    }


def test_valid_order(payload):
    assert Order(**payload).order_id == 1


@pytest.mark.parametrize(
    "field, bad_value",
    [
        ("quantity", 0),
        ("customer_email", "oops"),
        ("country", "XX"),
        ("status", "unknown"),
        ("order_date", "2999-01-01"),
    ],
)
def test_invalid_field(payload, field, bad_value):
    payload[field] = bad_value
    with pytest.raises(ValidationError):
        Order(**payload)


def test_inconsistent_total(payload):
    payload["total_amount"] = 999.0
    with pytest.raises(ValidationError):
        Order(**payload)
