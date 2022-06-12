from typing import List, Dict
from itertools import combinations
K = [['m', 'c', 'b'],
     ['m', 'p', 'j'],
     ['m', 'b'],
     ['c', 'j'],
     ['m', 'p', 'b'],
     ['m', 'c', 'b', 'j'],
     ['c', 'b', 'j'],
     ['b', 'c']]
SUPPORT_THRESHOLD = 0.26


def main():
    unique_values = find_unique_values(K)
    values_with_support = check_support(unique_values, K)

    generated_pairs = generate_dense_sets(values_with_support, 2)
    values_with_support = check_support(generated_pairs, K)

    generated_triples = generate_dense_sets(
        find_unique_values(values_with_support), 3)
    values_with_support = check_support(generated_triples, K)


def find_unique_values(list_to_search: List[str]) -> List[str]:
    unique_list: List[str] = []
    for sub_list in list_to_search:
        for element in sub_list:
            if element not in unique_list:
                unique_list.append(element)
    unique_list = sorted(unique_list)
    return unique_list


def check_support(unique_values: List[str], bucket_list: List[List[str]]) -> List[str]:
    values_to_check: Dict[str, int] = {}
    values_with_support: List[str] = []
    for value in unique_values:
        values_to_check[value] = 0

    for bucket in bucket_list:
        for key in values_to_check.keys():
            small_counter: int = 0
            for element in bucket:
                for sub_key in key:
                    if sub_key == element:
                        small_counter += 1
            if small_counter/len(key) == 1:
                values_to_check[key] += 1

    for key, value in values_to_check.items():
        if value / len(bucket_list) >= SUPPORT_THRESHOLD:
            values_with_support.append(key)

    print(f"C {values_to_check.keys()}")
    print(f"Values with support (L) {values_with_support} \n")
    return values_with_support


def generate_dense_sets(unique_values: List[str], size: int):
    unique_list = combinations(unique_values, size)
    return unique_list


main()

