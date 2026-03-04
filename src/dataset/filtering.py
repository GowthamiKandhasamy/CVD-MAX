from collections import defaultdict
from tqdm import tqdm
from .config import CNT_MIN_01, MAX_RATIO_0_1
from .similarity import compute_max_similarity


def group_by_cwe_project(data):
    """
    Groups data by (CWE, Project).
    Returns dictionary:
        key = (cwe, project)
        value = list of items
    """
    groups = defaultdict(list)

    for item in data:
        for cwe in item["cwe"]:
            key = (cwe, item["project"])
            groups[key].append(item)

    return groups


def rule_based_filtering(data):
    """
    Implements Algorithm 1 from MARCOVul paper:
    1. Remove groups with missing class.
    2. For imbalanced groups (ratio > MAX_RATIO_0_1),
       remove low-similarity non-vulnerable samples.
    """

    print("Grouping by (CWE, Project)...")
    groups = group_by_cwe_project(data)
    print(f"Total groups: {len(groups)}")

    del_idx_cwe = defaultdict(set)

    print("Applying rule-based filtering...")

    for (cwe, project), items in tqdm(groups.items()):

        cnt0 = sum(1 for i in items if i["target"] == 0)
        cnt1 = sum(1 for i in items if i["target"] == 1)

        # Rule 1: Remove groups with missing class
        if cnt0 < CNT_MIN_01 or cnt1 < CNT_MIN_01:
            for item in items:
                del_idx_cwe[item["idx"]].add(cwe)
            continue

        # Rule 2: Imbalance filtering
        if cnt0 / cnt1 > MAX_RATIO_0_1:

            del_num = cnt0 - cnt1 * MAX_RATIO_0_1

            vulnerable_funcs = [
                i["func"] for i in items if i["target"] == 1
            ]

            non_vul_items = [
                i for i in items if i["target"] == 0
            ]

            sim_scores = []

            for item in non_vul_items:
                sim = compute_max_similarity(
                    item["func"],
                    vulnerable_funcs
                )
                sim_scores.append((item["idx"], sim))

            # Sort by similarity (ascending = least similar first)
            sim_scores.sort(key=lambda x: x[1])

            # Remove lowest similarity non-vulnerable samples
            for idx, _ in sim_scores[:del_num]:
                del_idx_cwe[idx].add(cwe)

    print("Rebuilding filtered dataset...")

    new_data = []

    for item in data:
        if item["idx"] not in del_idx_cwe:
            new_data.append(item)
        else:
            # If multi-CWE, remove only specific CWE
            remaining_cwes = [
                c for c in item["cwe"]
                if c not in del_idx_cwe[item["idx"]]
            ]

            if remaining_cwes:
                item["cwe"] = remaining_cwes
                new_data.append(item)

    print(f"Remaining after rule-based filtering: {len(new_data)}")
    return new_data