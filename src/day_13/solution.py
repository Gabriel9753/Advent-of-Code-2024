import math
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict, deque, namedtuple
from datetime import datetime
from functools import lru_cache, reduce
from itertools import chain, combinations, permutations, product
import argparse

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

A_TOKENS = 3
B_TOKENS = 1


@timer(return_time=True)
def preprocess_input(input_data):
    # Preprocess the input data (if needed)
    input_data = [x.split(":")[1].strip() for x in input_data.splitlines() if x != ""]
    input_data = [list(map(int, re.findall(r"\d+", x))) for x in input_data]
    input_data = [input_data[i : i + 3] for i in range(0, len(input_data), 3)]
    return input_data


def is_near_int(x):
    return abs(x - round(x)) < 1e-3


def calc_inv(m):
    return np.linalg.inv(np.array([[m[0][0], m[1][0]], [m[0][1], m[1][1]]]))


def check_solvable(a, b):
    return all([is_near_int(a), is_near_int(b), 0 <= a, 0 <= b])


def calc_price(a, b):
    return A_TOKENS * int(round(a)) + B_TOKENS * int(round(b))


def solve(day_input, add):
    total = 0
    for m in day_input:
        a, b = calc_inv(m) @ (add + np.array(m[2]))
        total += calc_price(a, b) if check_solvable(a, b) else 0
    return total


@timer(return_time=True)
def task1(day_input):
    return solve(day_input, 0)


@timer(return_time=True)
def task2(day_input):
    return solve(day_input, 10000000000000)


def main(args):
    # Choose between the real input or the example input
    if args.example:
        day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    else:
        day_input = load_input(os.path.join(cur_dir, "input.txt"))

    day_input, t = preprocess_input(day_input)
    result_task1, time_task1 = task1(day_input)
    result_task2, time_task2 = task2(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    print(f"Processing data: {t:.6f} seconds")
    print(f"Task 1: {result_task1} ({time_task1:.6f} seconds)")
    print(f"Task 2: {result_task2} ({time_task2:.6f} seconds)")

    if args.timeit:
        avg_time_task1 = average_time(100, task1, day_input)
        avg_time_task2 = average_time(100, task2, day_input)
        print("\nAverage times:")
        print(f"Task 1: {avg_time_task1:.6f} seconds")
        print(f"Task 2: {avg_time_task2:.6f} seconds")
        write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", type=int, help="Use the example input", default=1)
    parser.add_argument("--timeit", type=int, help="Average the execution time over 100 runs", default=0)
    main(parser.parse_args())
