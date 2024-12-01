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
images_path = os.path.join(par_dir, "images")

delta_pos = {
    "up": lambda x, y: (x, y - 1),
    "right": lambda x, y: (x + 1, y),
    "down": lambda x, y: (x, y + 1),
    "left": lambda x, y: (x - 1, y),
}


def get_available_pos(grid, cur_x, cur_y):
    cur_symbol = grid[cur_y][cur_x]
    available_pos = []

    for d, f in delta_pos.items():
        new_x, new_y = f(cur_x, cur_y)
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            if d == "up" and cur_symbol in "S|LJ" and grid[new_y][new_x] in "S|F7":
                available_pos.append((new_x, new_y))
            if d == "right" and cur_symbol in "S-FL" and grid[new_y][new_x] in "S-J7":
                available_pos.append((new_x, new_y))
            if d == "down" and cur_symbol in "S|F7" and grid[new_y][new_x] in "S|LJ":
                available_pos.append((new_x, new_y))
            if d == "left" and cur_symbol in "S-J7" and grid[new_y][new_x] in "S-LF":
                available_pos.append((new_x, new_y))

    return available_pos


def print_grid(grid):
    for line in grid:
        print("".join(line))


@timer(return_time=True)
def task1(day_input):
    grid = [[c for c in line] for line in day_input.splitlines()]
    start_pos = (-1, -1)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "S":
                start_pos = (x, y)
                break

    visited = set()
    queue = deque()
    queue.append((start_pos, 0))
    while queue:
        cur_pos, cur_dist = queue.popleft()
        if cur_pos in [p[0] for p in visited]:
            continue
        visited.add((cur_pos, cur_dist))
        cur_x, cur_y = cur_pos
        for new_pos in get_available_pos(grid, cur_x, cur_y):
            queue.append((new_pos, cur_dist + 1))
    print(visited)
    return max([p[1] for p in visited])


@timer(return_time=True)
def task2(day_input):
    # Day-specific code for Task 2
    pass


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


if __name__ == "__main__":
    main()
