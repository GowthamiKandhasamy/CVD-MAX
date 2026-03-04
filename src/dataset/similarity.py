from rapidfuzz.distance import Levenshtein
import random


MAX_VUL_COMPARE = 20  # Cap vulnerable comparisons per group
LENGTH_DIFF_THRESHOLD = 0.8  # Skip if length differs too much


def compute_similarity(s1, s2):
    dist = Levenshtein.distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1 - (dist / max_len)


def compute_max_similarity(func, vulnerable_funcs):
    """
    Computes max similarity between func and a sampled subset of vulnerable functions.
    """

    if not vulnerable_funcs:
        return 0

    # Randomly sample vulnerable functions if too many
    if len(vulnerable_funcs) > MAX_VUL_COMPARE:
        vul_subset = random.sample(vulnerable_funcs, MAX_VUL_COMPARE)
    else:
        vul_subset = vulnerable_funcs

    max_sim = 0
    len_func = len(func)

    for v_func in vul_subset:
        len_v = len(v_func)

        # Length-based early rejection
        length_ratio = abs(len_func - len_v) / max(len_func, len_v)
        if length_ratio > LENGTH_DIFF_THRESHOLD:
            continue

        sim = compute_similarity(func, v_func)

        if sim > max_sim:
            max_sim = sim

    return max_sim