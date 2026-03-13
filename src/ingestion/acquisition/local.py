import shutil
import json
from pathlib import Path
from datetime import datetime

def acquire_from_local(project_name, local_path, architecture, raw_code_dir):
    project_dir = raw_code_dir / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(local_path, project_dir / "src", dirs_exist_ok=True)

    metadata = {
        "source_type": "local",
        "original_path": str(local_path),
        "architecture": architecture,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(project_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
