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

from util.general_util import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
CHAR_DICT = {"M": 1, "A": 2, "S": 3, "O": 0}


def search_letter_single(day_input, i, j, letter, direction):
    # search for the letter in the direction
    i += direction[0]
    j += direction[1]
    if 0 <= i < len(day_input) and 0 <= j < len(day_input[i]) and day_input[i][j] == letter:
        return True, (i, j)
    return False, (-1, -1)


def xmas_kernels(day_input):
    kernel_top = np.array(
        [
            [CHAR_DICT["M"], CHAR_DICT["O"], CHAR_DICT["M"]],
            [CHAR_DICT["O"], CHAR_DICT["A"], CHAR_DICT["O"]],
            [CHAR_DICT["S"], CHAR_DICT["O"], CHAR_DICT["S"]],
        ]
    )
    # Precompute all kernel rotations
    kernels = [kernel_top, np.rot90(kernel_top, 1), np.rot90(kernel_top, 2), np.rot90(kernel_top, 3)]

    transformed_day_input = np.array([
        [CHAR_DICT.get(char, CHAR_DICT["O"]) for char in row]
        for row in day_input
    ])

    xmas_count = 0

    pos_checks = [(0, 0), (0, 2), (2, 0), (2, 2)]

    for i in range(1, len(day_input) - 1):
        for j in range(1, len(day_input[i]) - 1):
            target_area = transformed_day_input[i - 1 : i + 2, j - 1 : j + 2]

            if target_area[1, 1] != CHAR_DICT['A']:
                continue

            border_chars = [
                target_area[0, 0], target_area[0, 2],
                target_area[2, 0], target_area[2, 2],
                target_area[1, 1]
            ]

            if CHAR_DICT['O'] in border_chars:
                continue

            if target_area[0, 0] == target_area[2, 2] or target_area[0, 2] == target_area[2, 0]:
                continue

            for kernel in kernels:
                if all(target_area[pos] == kernel[pos] for pos in pos_checks):
                    xmas_count += 1
                    break

    return xmas_count


@timer(return_time=True)
def task1(day_input):
    xmas_count = 0

    for i in range(len(day_input)):
        for j in range(len(day_input[i])):
            if day_input[i][j] == "X":
                for d in DIRS:
                    found_M, (i_M, j_M) = search_letter_single(day_input, i, j, "M", d)
                    if found_M:
                        found_A, (i_A, j_A) = search_letter_single(day_input, i_M, j_M, "A", d)
                        if found_A:
                            found_S, (i_S, j_S) = search_letter_single(day_input, i_A, j_A, "S", d)
                            if found_S:
                                xmas_count += 1

    return xmas_count


@timer(return_time=True)
def task2(day_input):
    return xmas_kernels(day_input)


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt"))
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    day_input = day_input.splitlines()

    # Call the tasks and store their results (if needed)
    result_task1, time_task1 = task1(day_input)
    result_task2, time_task2 = task2(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    # Print the results
    print("\nAnswers:")
    print(f"Task 1: {result_task1}")
    print(f"Task 2: {result_task2}")

    print("\nTimes:")
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")

    # 100 times and average the time
    avg_time_task1 = average_time(100, task1, day_input)
    avg_time_task2 = average_time(100, task2, day_input)
    print("\nAverage times:")
    print(f"Task 1: {avg_time_task1:.6f} seconds")
    print(f"Task 2: {avg_time_task2:.6f} seconds")
    write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    main()
