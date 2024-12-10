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

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

@timer(return_time=True)
def preprocess_input(input_data):
    # Preprocess the input data (if needed)
    _map = {
        (int(x), int(y)): int(val) if val != "." else -9
        for y, row in enumerate(input_data.splitlines())
        for x, val in enumerate(row)
    }
    start_coords = {c for c, val in _map.items() if val == 0}
    return (_map, start_coords)

def find_trails(day_input):
    _map = day_input[0]
    start_coords = day_input[1]

    # queue: (start, from)
    queue = deque([(c, c) for c in start_coords])
    trail_counter = defaultdict(list)

    while queue:
        start, _from = queue.pop()

        if _map[_from] == 9:
            trail_counter[start].append(_from)
        else:
            for dx, dy in DIRS:
                new_coords = (_from[0] + dx, _from[1] + dy)
                try:
                    if _map[new_coords] - _map[_from] == 1:
                        queue.append((start, new_coords))
                except KeyError:
                    pass

    return trail_counter


@timer(return_time=True)
def task1(day_input):
    return sum([len(set(trail)) for trail in find_trails(day_input).values()])


@timer(return_time=True)
def task2(day_input):
    return sum([len(trail) for trail in find_trails(day_input).values()])


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
