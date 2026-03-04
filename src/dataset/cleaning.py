from tqdm import tqdm
import re

def standardize_format(data):
    """
    Ensures each record has:
    idx, func, target, cwe (list), project
    """
    print("Standardizing data format...")

    standardized = []

    for idx, item in enumerate(tqdm(data)):
        try:
            func = item["func"]
            target = int(item["target"])
            project = item["project"]

            # Ensure CWE is list
            cwe_field = item["cwe"]
            if isinstance(cwe_field, list):
                cwe_list = cwe_field
            else:
                cwe_list = [cwe_field]

            standardized.append({
                "idx": idx,
                "func": func,
                "target": target,
                "cwe": cwe_list,
                "project": project
            })

        except KeyError:
            # skip malformed records
            continue

    print(f"Standardized {len(standardized)} records.")
    return standardized

def remove_duplicates(data):
    print("Removing duplicate functions...")

    seen = set()
    unique_data = []

    for item in data:
        func_hash = hash(item["func"])

        if func_hash not in seen:
            seen.add(func_hash)
            unique_data.append(item)

    print(f"Remaining after deduplication: {len(unique_data)}")
    return unique_data

def remove_missing_cwe(data):
    print("Removing entries with missing CWE...")

    filtered = [
        item for item in data
        if item["cwe"] and item["cwe"][0] not in [None, "", "Unknown"]
    ]

    print(f"Remaining after removing missing CWE: {len(filtered)}")
    return filtered

import re


def strip_comments(code):
    # Remove single-line comments
    code = re.sub(r'//.*', '', code)
    # Remove multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    return code


def extract_body(code):
    """
    Extract content inside outermost braces.
    """
    match = re.search(r'\{(.*)\}', code, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def is_trivial_function(func_code):
    """
    Detects trivial functions:
    - empty body
    - single return statement
    - only declaration
    - very low logic density
    """
    code = strip_comments(func_code)
    body = extract_body(code)

    if not body:
        return True

    # Remove whitespace
    body = body.strip()

    # Empty after stripping
    if body == "":
        return True

    # Only return statement
    if re.fullmatch(r'return\s+.*?;', body.strip()):
        return True

    # Count semicolons (rough proxy for statements)
    statements = [s for s in body.split(';') if s.strip()]

    if len(statements) <= 1:
        return True

    return False

def remove_trivial_functions(data):
    print("Removing trivial functions...")

    filtered = [
        item for item in data
        if not is_trivial_function(item["func"])
    ]

    print(f"Remaining after removing trivial functions: {len(filtered)}")
    return filtered