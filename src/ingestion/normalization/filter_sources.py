import json
import shutil
from src.ingestion.config import RAW_CODE_DIR, NORMALIZED_CODE_DIR


ALLOWED_EXTENSIONS = {".c", ".cpp", ".h", ".hpp"}

def normalize_sources(project_name):
    raw_root = RAW_CODE_DIR / project_name / "src"
    norm_root = NORMALIZED_CODE_DIR / project_name

    src_out = norm_root / "src"
    src_out.mkdir(parents=True, exist_ok=True)

    file_index = []

    for file in raw_root.rglob("*"):
        if file.suffix.lower() in ALLOWED_EXTENSIONS:
            rel_path = file.relative_to(raw_root)
            target = src_out / rel_path

            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)

            file_index.append(str(rel_path))

    with open(norm_root / "file_index.json", "w") as f:
        json.dump(file_index, f, indent=2)

    return norm_root
