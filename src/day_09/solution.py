from copy import deepcopy
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
    input_data = [
        (list(str(x) * int(x)), x, i) if i % 2 == 0 else (list("." * int(x)), x, i) for i, x in enumerate(input_data)
    ]
    file_system = []
    start_indices = dict()
    ptr = 0
    file_id = 0
    for i, x in enumerate(input_data):
        is_file = x[2] % 2 == 0
        start_indices[ptr] = (file_id, is_file, int(x[1]))
        file_system.extend([str(file_id) if is_file else "." for _ in range(int(x[1]))])
        ptr += len(x[0])
        file_id += 1 if is_file else 0
    input_data = (file_system, start_indices)
    return input_data


@timer(return_time=True)
def task1(day_input):

    def get_last_file_ptr(start_indices, last_keys):
        for i, k in enumerate(last_keys):
            if start_indices[k][1] and start_indices[k][2] > 0:
                return k, last_keys[i:]
        return -1, []

    # go through all free blocks and move the last file to the free block
    file_system, start_indices = day_input
    cp_file_system, cp_start_indices = deepcopy(file_system), deepcopy(start_indices)

    free_blocks = [i for i, x in enumerate(file_system) if x == "."]

    last_keys = list(cp_start_indices.keys())[::-1]
    for i in free_blocks:
        last_data_ptr, last_keys = get_last_file_ptr(cp_start_indices, last_keys)
        file = cp_start_indices[last_data_ptr]
        # 0: id, 1: is_file, 2: size
        if i >= last_data_ptr or file == -1:
            break
        cp_file_system[i] = str(file[0])
        cp_file_system[last_data_ptr + file[2] - 1] = "."
        new_file = (file[0], file[1], file[2] - 1)
        cp_start_indices[last_data_ptr] = new_file

    return sum([i * int(_id) for i, _id in enumerate(cp_file_system) if _id != "."])


@timer(return_time=True)
def task2(day_input):

    # go through all free blocks and move the last file to the free block
    file_system, start_indices = day_input
    cp_file_system, cp_start_indices = deepcopy(file_system), deepcopy(start_indices)

    free_blocks = []
    start = end = 0
    for i, x in enumerate(cp_file_system):
        if x == ".":
            if start == 0:
                start = i
            end = i
        else:
            if start != 0:
                free_blocks.append((start, end))
                start = end = 0

    sizes = [(end - start) + 1 for start, end in free_blocks]
    sizes = Counter(sizes)
    cur_min = min(sizes.keys())
    cur_max = max(sizes.keys())

    for ptr, file in list(cp_start_indices.items())[::-1]:
        if not file[1]:
            continue
        file_size = file[2]
        if file_size < cur_min or file_size > cur_max:
            continue
        for i, (start, end) in enumerate(free_blocks):
            if start > ptr:
                break

            free_size = (end - start) + 1
            if free_size < file_size:
                continue

            new_file_list = [str(file[0])] * file_size
            file_start, file_end = start, start + file_size - 1
            cp_file_system[file_start : file_end + 1] = new_file_list
            cp_file_system[ptr : ptr + file_size] = ["."] * file_size

            if end > file_end:
                free_blocks[i] = (file_end + 1, end)
            else:
                free_blocks.pop(i)

            left_over = free_size - file_size

            # update sizes and if it is the case, update cur_min and cur_max
            sizes[free_size] -= 1
            sizes[left_over] += 1

            if left_over < cur_min and sizes[left_over] <= 0:
                cur_min = left_over
            if left_over > cur_max and sizes[left_over] <= 0:
                cur_max = left_over
            break

    return sum([i * int(_id) for i, _id in enumerate(cp_file_system) if _id != "."])


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
