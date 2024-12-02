import math
import os
import re
import sys
from copy import deepcopy
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


def is_safe_diff(diff):
    return 1 <= diff <= 3

def is_in_order(is_increasing, v0, v1):
    return (is_increasing and v0 < v1) or (not is_increasing and v0 > v1)

def kernel(is_increasing, row, pivot):
    # check the pivot value in row and pivot-1, pivot+1
    # function returns true if the following conditions are met:
    # 1. the difference between the pivot and pivot-1 is >= 1 and <= 3
    # 2. the difference between the pivot and pivot+1 is >= 1 and <= 3
    # 3. the pivot value is in order with the increasing bool

    # if pivot is first or last element of row, then fill the missing value with a value that would meet the conditions
    v = row[pivot]
    v_left = row[pivot - 1] if pivot > 0 else v - 1 if is_increasing else v + 1
    v_right = row[pivot + 1] if pivot < len(row) - 1 else v + 1 if is_increasing else v - 1

    diff_left = abs(v - v_left)
    diff_right = abs(v - v_right)

    # check order
    if not is_in_order(is_increasing, v_left, v) or not is_in_order(is_increasing, v, v_right):
        return False


    if not is_safe_diff(diff_left) or not is_safe_diff(diff_right):
        return False

    return True

@timer(return_time=True)
def task1(day_input):
    unsafe_rows = 0
    increasing_rows = [day_input[i][0] < day_input[i][-1] for i in range(len(day_input))]

    for r, row in enumerate(day_input):
        is_increasing = increasing_rows[r]
        for i, num in enumerate(row):
            is_safe = kernel(is_increasing, row, i)
            if not is_safe:
                unsafe_rows += 1
                break

    return len(day_input) - unsafe_rows

@timer(return_time=True)
def task2(day_input):
    safe_values = deepcopy(day_input)
    # set all values to True
    for i, row in enumerate(safe_values):
        safe_values[i] = [True for _ in row]

    # first or last error could be the one problem we can remove
    # so, we have to check more values than just the first and last for increasing bool
    increasing_rows = []
    for r, row in enumerate(day_input):
        checks = [row[i] < row[i + 1] for i in range(4)]
        if checks.count(True) > checks.count(False):
            increasing_rows.append(True)
        else:
            increasing_rows.append(False)

    for r, row in enumerate(day_input):
        is_safe = True
        is_increasing = increasing_rows[r]
        unsafe_counter = 0

        for i, num in enumerate(row):
            is_safe = kernel(is_increasing, row, i)
            safe_values[r][i] = is_safe

            unsafe_counter += 1 if not is_safe else 0
            if unsafe_counter > 3:
                break

    safe_rows = 0

    # check again rows that have unsafe values (less than 4)
    for r, row in enumerate(safe_values):
        unsafe_values = sum([1 for v in row if not v])
        if unsafe_values == 0:
            safe_rows += 1
            continue

        if 0 < unsafe_values < 4:
            # remove all unsafe values iteratively and check then if the row is safe
            unsafe_indices = [i for i, v in enumerate(row) if not v]

            for i in unsafe_indices:
                row_copy = deepcopy(day_input[r])
                row_copy.pop(i)
                is_increasing = increasing_rows[r]
                is_safe = True

                for j, num in enumerate(row_copy):
                    is_safe = kernel(is_increasing, row_copy, j)
                    if not is_safe:
                        is_safe = False
                        break

                if is_safe:
                    safe_rows += 1
                    break

    return safe_rows


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt"))
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    day_input = [[int(x) for x in d.split()] for d in day_input.splitlines()]

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

    # 1000 times and average the time
    avg_time_task1 = average_time(1000, task1, day_input)
    avg_time_task2 = average_time(1000, task2, day_input)
    print("\nAverage times:")
    print(f"Task 1: {avg_time_task1:.6f} seconds")
    print(f"Task 2: {avg_time_task2:.6f} seconds")
    write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    main()
