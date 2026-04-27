# ==============================
# initiation
# ==============================
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
LOG_DIR = PROJECT_ROOT / "logs"
BACKUP_DIR = PROJECT_ROOT / "backup"

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from src.cleaner import clean_transactions
from src.data_loader import load_category_mapping, load_transactions
from src.feature_builder import build_features
from src.outlier_detector import flag_outliers_by_category_iqr
from src.paths import ensure_project_directories
from src.sample_data_builder import save_sample_data
from src.validator import validate_transactions_dataframe


RUN_DATE = "20260422"
RAW_FILEPATH = DATA_DIR / "raw" / f"transactions_sample_raw_{RUN_DATE}.csv"
MAPPING_FILEPATH = DATA_DIR / "metadata" / f"category_mapping_{RUN_DATE}.csv"
CLEANED_FILEPATH = DATA_DIR / "processed" / f"transactions_cleaned_int_{RUN_DATE}.csv"
FEATURED_FILEPATH = DATA_DIR / "processed" / f"transactions_featured_int_{RUN_DATE}.csv"
BACKUP_DIR_DATED = BACKUP_DIR / RUN_DATE


def main() -> None:
    ensure_project_directories()
    BACKUP_DIR_DATED.mkdir(parents=True, exist_ok=True)

    save_sample_data(RAW_FILEPATH, MAPPING_FILEPATH)
    DF_Raw = load_transactions(RAW_FILEPATH)
    DF_Mapping = load_category_mapping(MAPPING_FILEPATH)
    DF_Cleaned_int = clean_transactions(DF_Raw, DF_Mapping)
    DF_Featured_int = build_features(DF_Cleaned_int)
    DF_Featured_int = flag_outliers_by_category_iqr(DF_Featured_int)
    validate_transactions_dataframe(DF_Featured_int)

    DF_Cleaned_int.to_csv(CLEANED_FILEPATH, index=False)
    DF_Featured_int.to_csv(FEATURED_FILEPATH, index=False)
    DF_Raw.to_csv(BACKUP_DIR_DATED / RAW_FILEPATH.name, index=False)
    DF_Cleaned_int.to_csv(BACKUP_DIR_DATED / CLEANED_FILEPATH.name, index=False)
    DF_Featured_int.to_csv(BACKUP_DIR_DATED / FEATURED_FILEPATH.name, index=False)

    print(f"Artifacts built successfully on {datetime.now().isoformat(timespec='seconds')}")
    print(f"Raw rows: {len(DF_Raw)}")
    print(f"Cleaned rows: {len(DF_Cleaned_int)}")
    print(f"Featured rows: {len(DF_Featured_int)}")
    print(f"Outliers: {int(DF_Featured_int['OUTLIER_FLAG'].sum())}")


if __name__ == "__main__":
    main()
