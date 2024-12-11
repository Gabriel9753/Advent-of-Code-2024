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


@timer(return_time=True)
def preprocess_input(input_data):
    # Preprocess the input data (if needed)
    return list(map(int, input_data.split()))


@timer(return_time=True)
def task1(day_input):
    return 0
    blinks = 25
    differences = []

    for i in tqdm(range(blinks)):
        did_split = False
        for j, x in enumerate(day_input):
            if did_split:
                did_split = False
                continue
            if x == 0:
                day_input[j] = 1
            elif len(str(x)) % 2 == 0:
                str_x = str(x)
                len_x = len(str_x)
                half = len_x // 2
                first_half = str_x[:half]
                second_half = str_x[half:]
                day_input[j] = int(first_half)
                day_input.insert(j + 1, int(second_half))
                did_split = True
            else:
                day_input[j] *= 2024

    print(f"Diff: {differences}")

    return len(day_input)



@timer(return_time=True)
def task2(day_input):
    day_input = list(map(str, day_input))
    blinks = 25
    differences = []
    total_stones = 0

    for i, x in tqdm(enumerate(day_input)):
        for j in range(blinks):
            if int(x) == 0:
                x = "1"
            elif len(x) % 2 != 0:
                x = 2024 * int(x)
            else:
                pass

    return len(day_input)



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
