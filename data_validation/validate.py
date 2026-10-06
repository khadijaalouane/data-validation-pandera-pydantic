"""Script : sépare un CSV de commandes en lignes valides / invalides et produit un rapport.

Usage :
    python -m data_validation.validate data/orders_sample.csv
"""
import argparse

import pandas as pd
import pandera.pandas as pa

from .models import ValidationConfig
from .schemas import OrderSchema


def split_valid_invalid(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Retourne (lignes valides, lignes invalides, rapport détaillé des erreurs)."""
    try:
        return OrderSchema.validate(df, lazy=True), df.iloc[0:0], pd.DataFrame()
    except pa.errors.SchemaErrors as exc:
        failures = exc.failure_cases
        bad_index = failures["index"].dropna().unique()
        invalid = df.loc[df.index.isin(bad_index)]
        # Si l'erreur est globale (ex. colonne manquante), cette ligne relève l'erreur.
        valid = OrderSchema.validate(df.loc[~df.index.isin(bad_index)], lazy=True)
        return valid, invalid, failures


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path")
    parser.add_argument("--output-dir", default="output")
    args = parser.parse_args()

    config = ValidationConfig(input_path=args.input_path, output_dir=args.output_dir)
    config.output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(config.input_path)
    valid, invalid, failures = split_valid_invalid(df)

    valid.to_csv(config.output_dir / "valid_orders.csv", index=False)
    invalid.to_csv(config.output_dir / "invalid_orders.csv", index=False)
    failures.to_csv(config.output_dir / "failure_report.csv", index=False)

    print(f"Lignes lues      : {len(df)}")
    print(f"Lignes valides   : {len(valid)}")
    print(f"Lignes invalides : {len(invalid)}")
    if not failures.empty:
        print("\nErreurs par type de règle :")
        print(failures["check"].astype(str).value_counts().to_string())
    print(f"\nFichiers écrits dans : {config.output_dir}/")


if __name__ == "__main__":
    main()
