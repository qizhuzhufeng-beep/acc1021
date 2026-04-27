from __future__ import annotations

from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = [
    "TRANSACTION_ID",
    "DATE",
    "AMOUNT",
    "MERCHANT",
]


def validate_required_columns(DF_Input: pd.DataFrame, required_columns: Iterable[str] | None = None) -> None:
    RequiredColumns = list(required_columns or REQUIRED_COLUMNS)
    MissingColumns = [Column for Column in RequiredColumns if Column not in DF_Input.columns]
    if MissingColumns:
        raise ValueError(f"Missing required columns: {MissingColumns}")


def validate_amount_column(DF_Input: pd.DataFrame) -> None:
    if not pd.api.types.is_numeric_dtype(DF_Input["AMOUNT"]):
        raise ValueError("AMOUNT column must be numeric after cleaning.")


def validate_date_column(DF_Input: pd.DataFrame) -> None:
    if DF_Input["DATE"].isna().any():
        raise ValueError("DATE column contains unparseable values.")


def validate_transactions_dataframe(DF_Input: pd.DataFrame) -> None:
    validate_required_columns(DF_Input)
    validate_amount_column(DF_Input)
    validate_date_column(DF_Input)
