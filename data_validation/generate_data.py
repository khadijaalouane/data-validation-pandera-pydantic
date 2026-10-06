"""je génère un jeu de données de commandes avec des erreurs volontairement injectées.

Usage : python -m data_validation.generate_data
"""
import random
from datetime import datetime, timedelta

import pandas as pd

from .constants import COUNTRIES, STATUSES


def generate(n: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = random.Random(seed)
    start = datetime(2025, 1, 1)
    rows = []
    for i in range(1, n + 1):
        qty = rng.randint(1, 10)
        price = round(rng.uniform(5, 200), 2)
        rows.append(
            {
                "order_id": i,
                "customer_email": f"client{rng.randint(1, 80)}@example.com",
                "order_date": (start + timedelta(days=rng.randint(0, 365))).strftime("%Y-%m-%d"),
                "country": rng.choice(COUNTRIES),
                "quantity": qty,
                "unit_price": price,
                "total_amount": round(qty * price, 2),
                "status": rng.choice(STATUSES),
            }
        )
    df = pd.DataFrame(rows)

    # Injection d'erreurs sur des lignes distinctes
    picks = rng.sample(range(5, n), 14)
    df.loc[picks[0:2], "quantity"] = -3                       # quantité négative
    df.loc[picks[2:4], "customer_email"] = "not-an-email"     # email invalide
    df.loc[picks[4:6], "country"] = "XX"                      # pays inconnu
    df.loc[picks[6:8], "total_amount"] = 1.0                  # total incohérent
    df.loc[picks[8:10], "order_date"] = "2030-01-01"          # date future
    df.loc[picks[10:12], "unit_price"] = float("nan")         # prix manquant
    df.loc[picks[12], "order_id"] = int(df.loc[picks[12] - 1, "order_id"])  # doublon
    return df


if __name__ == "__main__":
    generate().to_csv("data/orders_sample.csv", index=False)
    print("data/orders_sample.csv généré")
