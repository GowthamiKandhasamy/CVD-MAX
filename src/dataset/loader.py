import json
from tqdm import tqdm
from .config import RAW_DATA_PATH


def load_raw_data():
    """
    Loads raw DiverseVul dataset from JSON or JSONL file.
    Returns list of records (dict).
    """
    print(f"Loading raw dataset from {RAW_DATA_PATH} ...")

    data = []

    with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
        first_char = f.read(1)
        f.seek(0)

        # Case 1: JSON array
        if first_char == "[":
            data = json.load(f)

        # Case 2: JSONL (one JSON per line)
        else:
            for line in tqdm(f):
                line = line.strip()
                if line:
                    data.append(json.loads(line))

    print(f"Loaded {len(data)} records.")
    return data