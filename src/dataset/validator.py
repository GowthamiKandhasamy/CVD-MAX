def validate_split(train, val, test):

    print("Validating dataset splits...")

    train_ids = {x["idx"] for x in train}
    val_ids = {x["idx"] for x in val}
    test_ids = {x["idx"] for x in test}

    assert train_ids.isdisjoint(val_ids)
    assert train_ids.isdisjoint(test_ids)
    assert val_ids.isdisjoint(test_ids)

    print("✔ No data leakage between splits")

    def count(data):
        vul = sum(1 for x in data if x["target"] == 1)
        non = sum(1 for x in data if x["target"] == 0)
        return vul, non

    tv, tn = count(train)
    vv, vn = count(val)
    tev, ten = count(test)

    print("\nSplit Statistics")
    print("----------------")
    print(f"Train: {len(train)} ({tv} vul / {tn} non)")
    print(f"Val:   {len(val)} ({vv} vul / {vn} non)")
    print(f"Test:  {len(test)} ({tev} vul / {ten} non)")