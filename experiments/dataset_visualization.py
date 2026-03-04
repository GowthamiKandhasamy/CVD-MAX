import json
import matplotlib.pyplot as plt
from collections import Counter

DATA_DIR = "data/processed"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


train = load_json(f"{DATA_DIR}/train.json")
val = load_json(f"{DATA_DIR}/val.json")
test = load_json(f"{DATA_DIR}/test.json")

all_data = train + val + test


# -------------------------------
# 1. Class Distribution
# -------------------------------

vul = sum(1 for x in all_data if x["target"] == 1)
non_vul = sum(1 for x in all_data if x["target"] == 0)

plt.figure()
plt.pie(
    [vul, non_vul],
    labels=["Vulnerable", "Non-Vulnerable"],
    autopct="%1.1f%%"
)
plt.title("Dataset Class Distribution")
plt.show()


# -------------------------------
# 2. Dataset Split Distribution
# -------------------------------

sizes = [len(train), len(val), len(test)]

plt.figure()
plt.bar(["Train", "Validation", "Test"], sizes)
plt.title("Dataset Split Sizes")
plt.ylabel("Number of Samples")
plt.show()


# -------------------------------
# 3. CWE Distribution
# -------------------------------

cwe_counter = Counter()

for item in all_data:
    for cwe in item["cwe"]:
        cwe_counter[cwe] += 1

top_cwe = dict(cwe_counter.most_common(10))

plt.figure()
plt.bar(top_cwe.keys(), top_cwe.values())
plt.title("Top 10 CWE Categories")
plt.xticks(rotation=45)
plt.ylabel("Number of Functions")
plt.show()


# -------------------------------
# 4. Project Distribution
# -------------------------------

project_counter = Counter(x["project"] for x in all_data)
top_projects = dict(project_counter.most_common(10))

plt.figure()
plt.bar(top_projects.keys(), top_projects.values())
plt.title("Top 10 Projects in Dataset")
plt.xticks(rotation=45)
plt.ylabel("Number of Functions")
plt.show()