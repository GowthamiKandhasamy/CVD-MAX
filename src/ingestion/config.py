from pathlib import Path

# Absolute path to project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_CODE_DIR = DATA_DIR / "raw_code"
NORMALIZED_CODE_DIR = DATA_DIR / "normalized_code"
