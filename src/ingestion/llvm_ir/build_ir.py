import json
import subprocess
from pathlib import Path
from datetime import datetime

from src.ingestion.config import (
    NORMALIZED_CODE_DIR,
    DATA_DIR
)

CLANG = "clang"
BASE_FLAGS = ["-S", "-emit-llvm", "-O0"]

def build_llvm_ir(project_name):
    norm_root = NORMALIZED_CODE_DIR / project_name
    src_root = norm_root / "src"
    selected_file = norm_root / "selected_files.json"

    out_root = DATA_DIR / "intermediate" / "llvm_ir" / project_name
    out_root.mkdir(parents=True, exist_ok=True)

    with open(selected_file) as f:
        files = json.load(f)

    compile_log = {}

    # Include root = normalized src root
    include_flags = [
    "-I", str(src_root),
    "-I", str(src_root / "expat" / "lib")
]

    for rel_path in files:
        if not rel_path.endswith((".c", ".cpp")):
            continue

        src_file = src_root / rel_path
        out_file = out_root / rel_path.replace("\\", "/")
        out_file = out_file.with_suffix(".ll")

        out_file.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            CLANG,
            *BASE_FLAGS,
            *include_flags,
            str(src_file),
            "-o",
            str(out_file)
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        compile_log[rel_path] = {
            "success": result.returncode == 0,
            "stderr": result.stderr
        }

        if result.returncode != 0:
            print(f"[LLVM-IR ERROR] {rel_path}")

    with open(out_root / "compile_meta.json", "w") as f:
        json.dump(
            {
                "project": project_name,
                "timestamp": datetime.utcnow().isoformat(),
                "results": compile_log
            },
            f,
            indent=2
        )

    return out_root
