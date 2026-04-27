from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
METADATA_DIR = DATA_DIR / "metadata"
CONFIG_DIR = PROJECT_ROOT / "config"
LOG_DIR = PROJECT_ROOT / "logs"
BACKUP_DIR = PROJECT_ROOT / "backup"


def ensure_project_directories() -> None:
    for Directory in [
        DATA_DIR,
        RAW_DIR,
        PROCESSED_DIR,
        METADATA_DIR,
        CONFIG_DIR,
        LOG_DIR,
        BACKUP_DIR,
    ]:
        Directory.mkdir(parents=True, exist_ok=True)
