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
    # 2d numpy map
    # return np.array([[x for x in row] for row in input_data.splitlines()])
    return {(x, y): z for y, row in enumerate(input_data.strip().splitlines()) for x, z in enumerate(row)}


@timer(return_time=True)
def task1(day_input):
    visited = set()
    plant_areas = []
    plant_perimeters = []

    queue = deque([[x, y, day_input[(x, y)]] for x, y in day_input])

    while queue:
        x, y, plant = queue.popleft()
        if (x, y, plant) in visited:
            continue
        visited.add((x, y, plant))

        plant_queue = deque([(x, y)])
        plant_area = [(x, y, plant)]
        plant_perimeter = 0

        while plant_queue:
            x, y = plant_queue.popleft()

            for dx, dy in DIRS:
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) in day_input and day_input[(new_x, new_y)] == plant and (new_x, new_y, plant) not in visited:
                    plant_queue.append((new_x, new_y))
                    visited.add((new_x, new_y, plant))
                    plant_area.append((new_x, new_y, plant))
                    continue
                if (new_x, new_y) not in day_input or day_input[(new_x, new_y)] != plant:
                    plant_perimeter += 1

        plant_areas.append(plant_area)
        plant_perimeters.append(plant_perimeter)

    return sum(len(p) * perimeter for p, perimeter in zip(plant_areas, plant_perimeters))

@timer(return_time=True)
def task2(day_input):
    visited = set()
    plant_areas = []
    plant_perimeters = []
    plant_edges = []

    queue = deque([[x, y, day_input[(x, y)]] for x, y in day_input])

    while queue:
        x, y, plant = queue.popleft()
        if (x, y, plant) in visited:
            continue
        visited.add((x, y, plant))

        plant_queue = deque([(x, y)])
        plant_area = [(x, y, plant)]
        plant_perimeter = 0

        while plant_queue:
            x, y = plant_queue.popleft()

            for dx, dy in DIRS:
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) in day_input and day_input[(new_x, new_y)] == plant and (new_x, new_y, plant) not in visited:
                    plant_queue.append((new_x, new_y))
                    visited.add((new_x, new_y, plant))
                    plant_area.append((new_x, new_y, plant))
                    continue
                if (new_x, new_y) not in day_input or day_input[(new_x, new_y)] != plant:
                    plant_perimeter += 1

        plant_areas.append(plant_area)
        plant_perimeters.append(plant_perimeter)
    # print(plant_areas)
    # print(plant_edges)

    plant_area_corners = []
    map_width = max(x for x, _ in day_input)
    map_height = max(y for _, y in day_input)

    map_corners = [(0, 0), (map_width, 0), (0, map_height), (map_width, map_height)]

    for plant_area in plant_areas:
        corners = []
        for plant in plant_area:
            x, y, p = plant
            same_plant_ctr = 0
            for dx, dy in DIRS:
                new_x, new_y = x + dx, y + dy
                new_p = day_input.get((new_x, new_y), None)
                if new_p == p:
                    same_plant_ctr += 1
            if same_plant_ctr < 3:
                corners.append((x,y))
                continue

            # if x,y are the corners of the map, also add as corner
            if (x, y) in map_corners:
                corners.append((x,y))

        plant_area_corners.append(corners)

    print(plant_area_corners)


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
