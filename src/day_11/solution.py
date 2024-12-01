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


def print_grid(grid):
    for row in grid:
        print("".join(row))


def get_grid_from_input(day_input):
    grid = []
    for line in day_input.splitlines():
        grid.append([c for c in line])
    return grid


def get_cols_rows_without_galaxies(grid):
    rows = []
    cols = []
    for i in range(len(grid)):
        if "#" not in grid[i]:
            rows.append(i)
    for j in range(len(grid[0])):
        if "#" not in [grid[i][j] for i in range(len(grid))]:
            cols.append(j)
    return rows, cols


def get_galaxies(grid):
    galaxies = []
    print(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "#":
                galaxies.append((i, j))
    return galaxies


def expand_grid(grid):
    rows, cols = get_cols_rows_without_galaxies(grid)
    for i in rows:
        grid.insert(i, ["." for _ in range(len(grid[0]))])
    for j in cols:
        for i in range(len(grid)):
            grid[i].insert(j, ".")
    return grid


@timer(return_time=True)
def task1(day_input):
    grid = day_input
    galaxies = get_galaxies(grid)
    print(galaxies)


@timer(return_time=True)
def task2(day_input):
    # Day-specific code for Task 2
    pass


def main():
    # Choose between the real input or the example input
    # day_input = load_input(os.path.join(cur_dir, "input.txt"))
    day_input = load_input(os.path.join(cur_dir, "example_input.txt"))

    grid = get_grid_from_input(day_input)
    grid = expand_grid(grid)
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
