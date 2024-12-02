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

@timer(return_time=True)
def task1(day_input):
    safe_rows = list(range(len(day_input)))
    increasing_rows = [day_input[i][0] < day_input[i][-1] for i in range(len(day_input))]

    for r, row in enumerate(day_input):
        is_safe = True
        is_increasing = increasing_rows[r]
        for i, num in enumerate(row):
            if i == 0:
                continue
            v0, v1 = row[i - 1], num
            diff = abs(v1 - v0)
            is_safe = is_safe_diff(diff) and is_in_order(is_increasing, v0, v1)
            if not is_safe:
                safe_rows.remove(r)
                break

    return len(safe_rows)


@timer(return_time=True)
def task2(day_input):
    copy_day_input = deepcopy(day_input)
    safe_rows = list(range(len(day_input)))
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
        rm_problems = 0

        for i, num in enumerate(row):
            if i == 0:
                continue
            v0, v1 = row[i - 1], num
            diff = abs(v1 - v0)
            is_safe = is_safe_diff(diff) and is_in_order(is_increasing, v0, v1)

            if not is_safe and rm_problems == 0:
                rm_problems += 1
                row[i] = v0
                # mark in copy_day_input that we have changed the value with a -inf
                copy_day_input[r][i] = -math.inf
                continue

            if not is_safe:
                safe_rows.remove(r)
                break

    print(copy_day_input)
    return len(safe_rows)


def main():
    # Choose between the real input or the example input
    # day_input = load_input(os.path.join(cur_dir, "input.txt"))
    day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
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
    # avg_time_task1 = average_time(1000, task1, day_input)
    # avg_time_task2 = average_time(1000, task2, day_input)
    # print("\nAverage times:")
    # print(f"Task 1: {avg_time_task1:.6f} seconds")
    # print(f"Task 2: {avg_time_task2:.6f} seconds")
    # write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    main()
