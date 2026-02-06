import subprocess
import shutil
import json
import os
import stat
from pathlib import Path
from datetime import datetime

def force_remove(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

import subprocess
import shutil
import json
import os
import stat
from pathlib import Path
from datetime import datetime

def force_remove(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def acquire_from_github(project_name, repo_url, commit_hash, architecture, raw_code_dir):
    project_dir = raw_code_dir / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    temp_dir = project_dir / "_tmp_clone"

    # 🔴 CRITICAL: clean up from previous failed runs
    if temp_dir.exists():
        shutil.rmtree(temp_dir, onerror=force_remove)

    subprocess.run(
        ["git", "clone", repo_url, str(temp_dir)],
        check=True
    )

    subprocess.run(
        ["git", "checkout", commit_hash],
        cwd=temp_dir,
        check=True
    )

    # Copy repo contents
    shutil.copytree(temp_dir, project_dir / "src", dirs_exist_ok=True)

    # Cleanup temp clone
    shutil.rmtree(temp_dir, onerror=force_remove)

    metadata = {
        "source_type": "github",
        "repo_url": repo_url,
        "commit_hash": commit_hash,
        "architecture": architecture,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(project_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
