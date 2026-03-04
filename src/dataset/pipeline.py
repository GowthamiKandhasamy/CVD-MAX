from .io_utils import save_json, load_json
from .partitioning import partition_dataset
from .validator import validate_split
from .config import PROCESSED_DIR, INTERIM_DIR


def print_stats(data, stage_name=""):
    vul = sum(1 for i in data if i["target"] == 1)
    non_vul = sum(1 for i in data if i["target"] == 0)

    print(f"\n=== {stage_name} ===")
    print(f"Total: {len(data)}")
    print(f"Vulnerable: {vul}")
    print(f"Non-vulnerable: {non_vul}")
    print(f"Ratio (0:1): {non_vul / vul:.2f}")


def print_dataset_metadata(data):
    unique_cwes = set()
    unique_projects = set()

    for item in data:
        for cwe in item["cwe"]:
            unique_cwes.add(cwe)
        unique_projects.add(item["project"])

    print("\n=== Dataset Metadata ===")
    print(f"Unique CWE types: {len(unique_cwes)}")
    print(f"Unique projects: {len(unique_projects)}")


def run_pipeline():

    # ---------------------------
    # Load Existing Filtered Dataset
    # ---------------------------
    print("Loading existing filtered dataset...")

    data = load_json(f"{INTERIM_DIR}/step5_filtered.json")

    print_stats(data, "Loaded Filtered Dataset")
    print_dataset_metadata(data)

    # ---------------------------
    # Stage 3: Partitioning
    # ---------------------------
    print("\nStarting dataset partitioning...")

    train, val, test = partition_dataset(data)

    print(f"Train size: {len(train)}")
    print(f"Validation size: {len(val)}")
    print(f"Test size: {len(test)}")

    # ---------------------------
    # Stage 4: Validation
    # ---------------------------
    validate_split(train, val, test)

    # ---------------------------
    # Save Final Splits
    # ---------------------------
    save_json(train, f"{PROCESSED_DIR}/train.json")
    save_json(val, f"{PROCESSED_DIR}/val.json")
    save_json(test, f"{PROCESSED_DIR}/test.json")

    print("\nSaved dataset splits to data/processed/")


if __name__ == "__main__":
    run_pipeline()