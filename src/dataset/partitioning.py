import random
from collections import defaultdict


def group_by_cwe_project(data):
    groups = defaultdict(list)

    for item in data:
        for cwe in item["cwe"]:
            groups[(cwe, item["project"])].append(item)

    return groups


import random


def partition_dataset(data, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):

    data_copy = data.copy()
    random.shuffle(data_copy)

    n = len(data_copy)

    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)

    train = data_copy[:train_end]
    val = data_copy[train_end:val_end]
    test = data_copy[val_end:]

    return train, val, test