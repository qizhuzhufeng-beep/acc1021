from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.validator import validate_required_columns


def load_transactions(filepath: str | Path) -> pd.DataFrame:
    FilePath = Path(filepath)
    DF_Raw = pd.read_csv(FilePath)
    DF_Raw.columns = [Column.strip().upper() for Column in DF_Raw.columns]
    validate_required_columns(DF_Raw)
    return DF_Raw


def load_category_mapping(filepath: str | Path) -> pd.DataFrame:
    FilePath = Path(filepath)
    DF_Mapping = pd.read_csv(FilePath)
    DF_Mapping.columns = [Column.strip().upper() for Column in DF_Mapping.columns]
    return DF_Mapping
