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
from rich import print

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")

# set recursion limit to maximum
sys.setrecursionlimit(10 ** 6)

DIRS = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}
ROTATION_COST = 1000


@timer(return_time=True)
def preprocess_input(input_data):
    # Preprocess the input data (if needed)
    _map = {(x, y): char for y, line in enumerate(input_data.splitlines()) for x, char in enumerate(line)}
    start = next(k for k, v in _map.items() if v == "S")
    end = next(k for k, v in _map.items() if v == "E")
    return _map, start, end


@timer(return_time=True)
def task1(day_input):
    maze_map, start, end = day_input
    cur_lowest_cost = math.inf
    queue = deque([(start, DIRS["E"], 0, [start])])
    visited = defaultdict(lambda: cur_lowest_cost)
    best_paths = []

    while queue:
        pos, direction, cost, path = queue.popleft()

        if pos == end:
            if cost < cur_lowest_cost:
                cur_lowest_cost = cost
                best_paths = [path]
            elif cost == cur_lowest_cost:
                best_paths.append(path)
            continue

        if visited[(pos, direction)] < cost:
            continue
        visited[(pos, direction)] = cost

        for new_dir in DIRS.values():
            if direction == (-new_dir[0], -new_dir[1]):
                continue
            new_costs = cost + ROTATION_COST if new_dir != direction else cost + 1
            if new_costs > cur_lowest_cost:
                continue

            if new_dir != direction:
                queue.append((pos, new_dir, new_costs, path))
            else:
                new_pos = tuple(map(sum, zip(pos, new_dir)))
                if new_pos in maze_map and maze_map[new_pos] != "#":
                    queue.append((new_pos, new_dir, new_costs, path + [new_pos]))

    return cur_lowest_cost, len(set([pos for path in best_paths for pos in path]))


def main(args):
    # Choose between the real input or the example input
    if args.example:
        day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    else:
        day_input = load_input(os.path.join(cur_dir, "input.txt"))

    day_input, t = preprocess_input(day_input)
    (result_task1, result_task2), time_task1 = task1(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    print(f"Processing data: {t:.6f} seconds")
    print(f"Task 1: {result_task1} ({time_task1:.6f} seconds)")
    print(f"Task 2: {result_task2} ({time_task1:.6f} seconds)")

    if args.timeit:
        avg_time_task1 = average_time(100, task1, day_input)
        print("\nAverage times:")
        print(f"Task 1: {avg_time_task1:.6f} seconds")
        print(f"Task 2: {avg_time_task1:.6f} seconds")
        write_times_to_readme(cur_day, avg_time_task1, avg_time_task1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", type=int, help="Use the example input", default=1)
    parser.add_argument("--timeit", type=int, help="Average the execution time over 100 runs", default=0)
    main(parser.parse_args())
