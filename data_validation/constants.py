"""Règles métier partagées : une seule source de vérité pour pandera ET pydantic."""
from typing import Literal, get_args

Country = Literal["MA", "FR", "ES", "DE", "US"]
Status = Literal["pending", "shipped", "delivered", "cancelled"]

COUNTRIES = list(get_args(Country))
STATUSES = list(get_args(Status))

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
MAX_QUANTITY = 100
