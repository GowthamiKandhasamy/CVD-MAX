"""
CVD-MAX Pipeline Entrypoint (Static Ingestion)

Stages:
1. Code Acquisition
2. Source Normalization
3. Source Selection
4. LLVM IR Generation

This script intentionally does NOT commit any data.
All artifacts are generated under /data and ignored by Git.
"""

from src.ingestion.acquisition.acquire import acquire_code
from src.ingestion.normalization.filter_sources import normalize_sources
from src.ingestion.selection.select_sources import select_sources
from src.ingestion.llvm_ir.build_ir import build_llvm_ir


def run_static_ingestion(
    project_name: str,
    source_type: str,
    architecture: str,
    repo_url: str | None = None,
    commit_hash: str | None = None,
    local_path: str | None = None,
):
    print(f"\n=== CVD-MAX Static Ingestion: {project_name} ===\n")

    # 1. Code Acquisition
    print("[1/4] Acquiring source code...")
    acquire_code(
        source_type=source_type,
        project_name=project_name,
        repo_url=repo_url,
        commit_hash=commit_hash,
        local_path=local_path,
        architecture=architecture,
    )

    # 2. Normalization
    print("[2/4] Normalizing source files...")
    normalize_sources(project_name)

    # 3. Source Selection
    print("[3/4] Selecting production source files...")
    selected = select_sources(project_name)
    print(f"      Selected {len(selected)} translation units")

    # 4. LLVM IR Generation
    print("[4/4] Generating LLVM IR...")
    build_llvm_ir(project_name)

    print("\n=== Static ingestion complete ===")
    print("LLVM IR available under:")
    print(f"data/intermediate/llvm_ir/{project_name}/\n")


if __name__ == "__main__":
    # ---- DEMO CONFIGURATION ----
    run_static_ingestion(
        project_name="test_proj",
        source_type="github",
        repo_url="https://github.com/libexpat/libexpat",
        commit_hash="master",
        architecture="x86_64",
    )
