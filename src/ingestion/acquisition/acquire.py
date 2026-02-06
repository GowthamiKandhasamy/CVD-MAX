from .github import acquire_from_github
from .local import acquire_from_local

from src.ingestion.config import RAW_CODE_DIR

def acquire_code(**kwargs):
    source_type = kwargs["source_type"]
    project_name = kwargs["project_name"]

    if source_type == "github":
        acquire_from_github(
            project_name,
            kwargs["repo_url"],
            kwargs["commit_hash"],
            kwargs["architecture"],
            RAW_CODE_DIR
        )

    elif source_type == "local":
        acquire_from_local(
            project_name,
            kwargs["local_path"],
            kwargs["architecture"],
            RAW_CODE_DIR
        )

    else:
        raise ValueError("Unsupported source type")
