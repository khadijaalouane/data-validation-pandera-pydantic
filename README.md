# Data Validation avec pandera et pydantic

Mini-projet qui montre comment **valider la qualité de données** avant de les utiliser dans un pipeline de data science / machine learning.

- **pandera** valide un **DataFrame entier** (types, plages de valeurs, unicité, règles entre colonnes).
- **pydantic** valide **un enregistrement à la fois** (ex. payload d'API) et la configuration du script.
- Les règles métier sont définies **une seule fois** (`constants.py`) et réutilisées par les deux outils.

## Cas d'usage

Un fichier de commandes e-commerce (`data/orders_sample.csv`, 200 lignes) contient des erreurs volontaires : quantités négatives, emails invalides, pays inconnus, totaux incohérents, dates futures, prix manquants, doublons. Le script sépare les lignes valides des lignes invalides et produit un rapport d'erreurs.

## Règles de validation

| Colonne | Règle |
|---|---|
| `order_id` | entier > 0, unique |
| `customer_email` | format email valide |
| `order_date` | date valide, pas dans le futur |
| `country` | MA, FR, ES, DE, US |
| `quantity` | entier entre 1 et 100 |
| `unit_price` | nombre > 0, non nul |
| `total_amount` | = `quantity` × `unit_price` (tolérance 0,01) |
| `status` | pending, shipped, delivered, cancelled |

Les colonnes inattendues sont refusées (`strict=True`).

## Structure

```
data_validation/
  constants.py       règles métier partagées
  schemas.py         schéma pandera (DataFrame)
  models.py          modèles pydantic (enregistrement + config)
  validate.py        script de validation en ligne de commande
  generate_data.py   génération des données de test
tests/               tests pytest
data/orders_sample.csv
.github/workflows/ci.yml   tests automatiques à chaque push
```

## Installation

```bash
git clone https://github.com/khadijaalouane/data-validation-pandera-pydantic.git
cd data-validation-pandera-pydantic
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation

Valider un fichier :

```bash
python -m data_validation.validate data/orders_sample.csv
```

Résultats dans `output/` : `valid_orders.csv`, `invalid_orders.csv`, `failure_report.csv`.

Valider un enregistrement avec pydantic :

```python
from data_validation.models import Order

Order(order_id=1, customer_email="a@example.com", order_date="2025-01-10",
      country="MA", quantity=2, unit_price=10.0, total_amount=20.0, status="pending")
```

Lancer les tests :

```bash
pytest
```

## Choix techniques

- `lazy=True` dans pandera : toutes les erreurs sont collectées en une passe au lieu de s'arrêter à la première.
- `coerce=True` : les types sont convertis quand c'est possible (ex. dates lues comme texte).
- Un `Literal` Python sert de source unique pour les pays et statuts, utilisés par pandera et pydantic.

## Pistes d'amélioration

- Ajouter des règles statistiques (détection de valeurs aberrantes, dérive de distribution)
- Exposer la validation via une API FastAPI
- Générer un rapport HTML des erreurs
- Intégrer la validation dans un pipeline d'entraînement de modèle
