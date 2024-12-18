from copy import deepcopy
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

PATTERN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


@timer(return_time=True)
def task1(day_input):
    return sum([int(a) * int(b) for a, b in PATTERN.findall(day_input)])


@timer(return_time=True)
def task2(day_input):
    pattern = re.compile(PATTERN)
    indexes_mul = [("m", m.start(), m.end()) for m in re.finditer(PATTERN, day_input)]
    indexes_do = [("y", m.start()) for m in re.finditer(r"do\(\)", day_input)]
    indexes_dont = [("n", m.start()) for m in re.finditer("don't\(\)", day_input)]
    all_indexes = indexes_do + indexes_dont + indexes_mul
    all_indexes.sort(key=lambda x: x[1])

    # mul if state is 1. Switch state to 0 if dont is found. Switch state to 1 if do is found
    state = 1
    res = 0

    for i in all_indexes:
        if i[0] == "m" and state == 1:
            mul_nums = pattern.findall(day_input[i[1] : i[2]])
            res += int(mul_nums[0][0]) * int(mul_nums[0][1])
        state = 1 if i[0] == "y" else 0 if i[0] == "n" else state

    return res


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
