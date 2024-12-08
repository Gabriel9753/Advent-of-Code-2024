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
    # create 2d dict with the values of the input
    input_data = {
        col: {row: val for row, val in enumerate(row_data)} for col, row_data in enumerate(input_data.split("\n"))
    }
    antennas = defaultdict(list)
    for col, row_data in input_data.items():
        for row, val in row_data.items():
            if val != ".":
                antennas[val].append((col, row))

    return input_data, antennas


def get_antinodes(x, y, x1, y1, dx, dy, in_grid):
    antinodes_x_coords = [x - dx, x1 + dx] if x < x1 else [x + dx, x1 - dx]
    antinodes_y_coords = [y - dy, y1 + dy] if y < y1 else [y + dy, y1 - dy]
    antinode1 = (antinodes_x_coords[0], antinodes_y_coords[0])
    antinode2 = (antinodes_x_coords[1], antinodes_y_coords[1])

    antinodes = set()
    if in_grid(*antinode1):
        antinodes.add(antinode1)
    if in_grid(*antinode2):
        antinodes.add(antinode2)

    return antinodes


@timer(return_time=True)
def task1(day_input):
    input_data, antennas = day_input
    width, height = len(input_data), len(input_data[0])

    def in_grid(x, y):
        return 0 <= x < width and 0 <= y < height

    antinodes = set()

    for _, coords in antennas.items():
        queue = deque(coords)
        while queue:
            x, y = queue.popleft()
            others = set(queue)
            for other in others:
                x1, y1 = other
                dx, dy = abs(x - x1), abs(y - y1)
                antinodes |= get_antinodes(x, y, x1, y1, dx, dy, in_grid)

    return len(antinodes)


def get_more_antinodes(x, y, x1, y1, dx, dy, in_grid):
    antinodes = set([(x, y), (x1, y1)])

    i = 0
    while True:
        i += 1
        antinodes_x_coords = [x - dx * i, x1 + dx * i] if x < x1 else [x + dx * i, x1 - dx * i]
        antinodes_y_coords = [y - dy * i, y1 + dy * i] if y < y1 else [y + dy * i, y1 - dy * i]
        antinode1 = (antinodes_x_coords[0], antinodes_y_coords[0])
        antinode2 = (antinodes_x_coords[1], antinodes_y_coords[1])

        do_continue = False
        if in_grid(*antinode1):
            antinodes.add(antinode1)
            do_continue = True
        if in_grid(*antinode2):
            antinodes.add(antinode2)
            do_continue = True

        if not do_continue:
            break

    return antinodes


@timer(return_time=True)
def task2(day_input):
    input_data, antennas = day_input
    width, height = len(input_data), len(input_data[0])

    def in_grid(x, y):
        return 0 <= x < width and 0 <= y < height

    antinodes = set()

    for _, coords in antennas.items():
        queue = deque(coords)
        while queue:
            x, y = queue.popleft()
            others = set(queue)
            for other in others:
                x1, y1 = other
                dx, dy = abs(x - x1), abs(y - y1)
                antinodes |= get_more_antinodes(x, y, x1, y1, dx, dy, in_grid)

    return len(antinodes)


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
