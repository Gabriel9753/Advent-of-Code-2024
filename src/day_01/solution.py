import math
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict, deque, namedtuple
from datetime import datetime
from functools import lru_cache, reduce
from itertools import chain, combinations, permutations, product

import numpy as np
from tqdm import tqdm

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import load_input, timer

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day

spelled_numbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


@timer(return_time=True)
def task1(day_input):
    # Day-specific code for Task 1
    calibration_sum = 0
    lines = day_input.split("\n")

    for line in lines:
        first_digit, last_digit = None, None

        for _char in line:
            # first occurrence of a digit
            if _char.isnumeric() and first_digit is None:
                first_digit = int(_char)
                last_digit = int(_char)
            # every other occurrence of a digit, so last_digit is always the last digit
            elif _char.isnumeric():
                last_digit = int(_char)

        if first_digit is not None and last_digit is not None:
            calibration_sum += int(f"{first_digit}{last_digit}")

    return calibration_sum


@timer(return_time=True)
def task2(day_input):
    # Day-specific code for Task 2

    calibration_sum = 0
    lines = day_input.split("\n")

    # pattern_str = all digits or spelled out words defined in the dictionary above
    pattern_str = f"(\d)|(?=({'|'.join(spelled_numbers.keys())}))"
    pattern = re.compile(pattern_str)

    for line in lines:
        matches = pattern.finditer(line)
        matches = [match.groups() for match in matches]
        matches = [match[0] if match[0] is not None else match[1] for match in matches]
        matches = [
            match if match.isnumeric() else spelled_numbers[match] for match in matches
        ]
        calibration_sum += int(f"{matches[0]}{matches[-1]}") if len(matches) > 0 else 0

    return calibration_sum


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt"))
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt"))

    # Call the tasks and store their results (if needed)
    result_task1, time_task1 = task1(day_input)
    result_task2, time_task2 = task2(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    # Print the results
    print("\nAnswers:")
    print(f"Task 1: {result_task1}")  # 54940
    print(f"Task 2: {result_task2}")  # 54208

    print("\nTimes:")
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")


if __name__ == "__main__":
    main()
