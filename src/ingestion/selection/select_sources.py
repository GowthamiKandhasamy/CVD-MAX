import json
from pathlib import Path

def select_sources(project_name):
    norm_root = Path("data/normalized_code") / project_name
    index_path = norm_root / "file_index.json"

    with open(index_path) as f:
        files = json.load(f)

    selected = []

    for path in files:
        p = path.replace("\\", "/")  # Windows safety

        if "/lib/" in p and not any(x in p for x in ["/tests/", "/examples/", "/fuzz/"]):
            selected.append(path)

    with open(norm_root / "selected_files.json", "w") as f:
        json.dump(selected, f, indent=2)

    return selected
