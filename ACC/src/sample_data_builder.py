from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


CATEGORY_CONFIG = {
    "Food & Beverage": {
        "weight": 0.35,
        "subcategories": ["Coffee", "Meal", "Takeout", "Dessert"],
        "merchants": ["Starbucks", "Mcdonalds", "Mixue", "Campus Cafe", "Foodpanda"],
        "amount_range": (6, 38),
        "necessity": "Non-essential",
    },
    "Transport": {
        "weight": 0.15,
        "subcategories": ["Ride", "Train", "Bus"],
        "merchants": ["Grab", "Rapidkl", "Mrt", "Tng Reload"],
        "amount_range": (5, 42),
        "necessity": "Necessary",
    },
    "Groceries": {
        "weight": 0.12,
        "subcategories": ["Supermarket", "Household"],
        "merchants": ["Tesco", "Lotus", "Aeon", "Jaya Grocer"],
        "amount_range": (18, 135),
        "necessity": "Necessary",
    },
    "Shopping": {
        "weight": 0.15,
        "subcategories": ["Clothing", "Online Shopping", "Electronics"],
        "merchants": ["Uniqlo", "Shopee", "Muji", "Apple Reseller"],
        "amount_range": (24, 260),
        "necessity": "Non-essential",
    },
    "Entertainment": {
        "weight": 0.08,
        "subcategories": ["Movie", "Gaming", "Subscription"],
        "merchants": ["Netflix", "Tgv", "Steam", "Spotify"],
        "amount_range": (12, 80),
        "necessity": "Non-essential",
    },
    "Bills": {
        "weight": 0.08,
        "subcategories": ["Phone", "Internet", "Utilities"],
        "merchants": ["Maxis", "Celcomdigi", "Unifi", "Tnb"],
        "amount_range": (35, 180),
        "necessity": "Necessary",
    },
    "Education": {
        "weight": 0.04,
        "subcategories": ["Books", "Printing", "Course Fee"],
        "merchants": ["Bookxcess", "Campus Print", "Udemy"],
        "amount_range": (10, 160),
        "necessity": "Necessary",
    },
    "Health": {
        "weight": 0.03,
        "subcategories": ["Clinic", "Pharmacy", "Fitness"],
        "merchants": ["Guardian", "Watsons", "Campus Clinic"],
        "amount_range": (12, 120),
        "necessity": "Necessary",
    },
}


def build_category_mapping_dataframe() -> pd.DataFrame:
    Records = []
    for Category, Config in CATEGORY_CONFIG.items():
        for Merchant in Config["merchants"]:
            Keyword = Merchant.lower()
            Records.append(
                {
                    "KEYWORD": Keyword,
                    "CATEGORY": Category,
                    "SUBCATEGORY": Config["subcategories"][0],
                    "NECESSITY_FLAG": Config["necessity"],
                }
            )
    return pd.DataFrame(Records)


def generate_transactions(seed: int = 42, start_date: str = "2025-05-01", months: int = 12, transaction_count: int = 520) -> pd.DataFrame:
    Rng = np.random.default_rng(seed)
    StartDate = pd.Timestamp(start_date)
    EndDate = StartDate + pd.DateOffset(months=months) - pd.DateOffset(days=1)
    DateRange = pd.date_range(StartDate, EndDate, freq="D")

    Categories = list(CATEGORY_CONFIG.keys())
    Weights = [CATEGORY_CONFIG[Category]["weight"] for Category in Categories]
    Records = []

    for TransactionIndex in range(transaction_count):
        Category = Rng.choice(Categories, p=Weights)
        Config = CATEGORY_CONFIG[Category]
        DateValue = pd.Timestamp(Rng.choice(DateRange))
        IsWeekend = DateValue.dayofweek >= 5
        Merchant = str(Rng.choice(Config["merchants"]))
        Subcategory = str(Rng.choice(Config["subcategories"]))
        Amount = float(Rng.uniform(*Config["amount_range"]))

        if IsWeekend and Category in ["Food & Beverage", "Entertainment", "Shopping"]:
            Amount *= 1.15
        if DateValue.month in [10, 11] and Category == "Shopping":
            Amount *= 1.20
        if DateValue.month in [12] and Category == "Food & Beverage":
            Amount *= 1.10

        Records.append(
            {
                "TRANSACTION_ID": f"TXN{TransactionIndex + 1:04d}",
                "DATE": DateValue.strftime("%Y-%m-%d"),
                "AMOUNT": round(max(Amount, 3), 2),
                "CURRENCY": "CNY",
                "CATEGORY": "",
                "SUBCATEGORY": "",
                "MERCHANT": Merchant,
                "PAYMENT_METHOD": str(Rng.choice(["Cash", "Card", "E-wallet"], p=[0.15, 0.45, 0.40])),
                "NECESSITY_FLAG": "",
                "LOCATION": str(Rng.choice(["On Campus", "Off Campus", "Online"], p=[0.35, 0.40, 0.25])),
                "NOTES": "",
                "USER_TAG": "",
            }
        )

    DF_Raw = pd.DataFrame(Records)

    OutlierRows = [
        ("2025-07-14", 489.0, "Apple Reseller", "New keyboard"),
        ("2025-09-03", 420.0, "Shopee", "Flash sale haul"),
        ("2025-10-21", 365.0, "Grab", "Airport commute"),
        ("2025-12-02", 540.0, "Uniqlo", "Holiday wardrobe"),
        ("2026-02-17", 610.0, "Apple Reseller", "Tablet purchase"),
    ]
    for Offset, (DateValue, Amount, Merchant, NotesValue) in enumerate(OutlierRows, start=1):
        DF_Raw.loc[len(DF_Raw)] = {
            "TRANSACTION_ID": f"TXN_OUTLIER_{Offset:02d}",
            "DATE": DateValue,
            "AMOUNT": Amount,
            "CURRENCY": "CNY",
            "CATEGORY": "",
            "SUBCATEGORY": "",
            "MERCHANT": Merchant,
            "PAYMENT_METHOD": "Card",
            "NECESSITY_FLAG": "",
            "LOCATION": "Online",
            "NOTES": NotesValue,
            "USER_TAG": "Outlier",
        }

    return DF_Raw.sort_values("DATE").reset_index(drop=True)


def save_sample_data(raw_path: Path, mapping_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    DF_Raw = generate_transactions()
    DF_Mapping = build_category_mapping_dataframe()
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    DF_Raw.to_csv(raw_path, index=False)
    DF_Mapping.to_csv(mapping_path, index=False)
    return DF_Raw, DF_Mapping
