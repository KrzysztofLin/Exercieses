from typing import Dict, List


STREAM = ['a', 'b', 'c', 'b', 'd', 'a', 'c', 'd', 'a', 'b', 'd', 'c', 'a', 'a', 'b']

def timestamps_collector(k_variables: int) -> List[int]:
    timestamp_list = []
    for i in range(1, k_variables + 1):
        timestamp_list.append(int(input(f"Insert timestamp {i}: ")))
    timestamp_list = sorted(timestamp_list) + [0]
    return timestamp_list
    

def calculate_value_in_stream(STREAM, timestamp_list: (List[str], List[int])) -> tuple[dict[str, int], int]:
    stream_variables = {}
    bottom_boundary = timestamp_list[0]
    stream_length = len(STREAM)
    for index in range(bottom_boundary, stream_length):
        if index == timestamp_list[0]:
            stream_variables[STREAM[index]] = 1
            timestamp_list.pop(0)
        elif STREAM[index] in stream_variables:
            stream_variables[STREAM[index]] += 1
        else:
            pass
    return stream_variables, stream_length


def surprise_number_calculator(stream_variables, stream_length, k_variables: (Dict[str, int], int, int)) -> None:
    surprise_value = 0
    for value in stream_variables.values():
        surprise_value += (stream_length-1) * (2*value - 1)
    print (surprise_value/k_variables)


def main(STREAM: List[str]) -> None:
    STREAM = ['x'] + STREAM
    k_variables = int(input("Input the number of variables which you would like to follow: "))
    timestamp_list = timestamps_collector(k_variables)
    stream_variables, stream_length = calculate_value_in_stream(STREAM, timestamp_list)
    surprise_number_calculator(stream_variables, stream_length, k_variables)


main(STREAM)
