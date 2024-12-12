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
RIGHT, LEFT, UP, DOWN = 0, 1, 2, 3

@timer(return_time=True)
def preprocess_input(input_data):
    # Preprocess the input data (if needed)
    # 2d numpy map
    # return np.array([[x for x in row] for row in input_data.splitlines()])
    return {(x, y): z for y, row in enumerate(input_data.strip().splitlines()) for x, z in enumerate(row)}


def analyze_areas(day_input):
    visited = set()
    plant_areas = []
    plant_edges = []
    queue = deque([[x, y, day_input[(x, y)]] for x, y in day_input])

    while queue:
        x, y, plant = queue.popleft()
        if (x, y, plant) in visited:
            continue
        visited.add((x, y, plant))

        plant_queue = deque([(x, y)])
        plant_area = [(x, y, plant)]
        edges = set()

        while plant_queue:
            x, y = plant_queue.popleft()

            for dx, dy in DIRS:
                new_x, new_y = x + dx, y + dy
                if (
                    (new_x, new_y) in day_input
                    and day_input[(new_x, new_y)] == plant
                    and (new_x, new_y, plant) not in visited
                ):
                    plant_queue.append((new_x, new_y))
                    visited.add((new_x, new_y, plant))
                    plant_area.append((new_x, new_y, plant))
                    continue
                if (new_x, new_y) not in day_input or day_input[(new_x, new_y)] != plant:
                    edges.add((new_x, new_y, (dx, dy)))

        plant_edges.append(edges)
        plant_areas.append(plant_area)
    return plant_areas, plant_edges


@timer(return_time=True)
def task1(day_input):
    plant_areas, plant_edges = analyze_areas(day_input)

    return sum(len(p) * len(set(edges)) for p, edges in zip(plant_areas, plant_edges))


def walk_line(day_input, p, line_coord_to_modify, edge_coords, visited, go_horizontal, side, x, y, dx=0, dy=0):
    i = 0
    other_side = RIGHT if side == LEFT else LEFT if side == RIGHT else UP if side == DOWN else DOWN
    while True:
        i += 1
        new_x, new_y = x + (i * dx), y + (i * dy)

        if (new_x, new_y) not in edge_coords:
            break

        # check if other side is the correct plant p or if it is a plant from another area
        if other_side == RIGHT:
            if (new_x + 1, new_y) in day_input and day_input[(new_x + 1, new_y)] != p:
                break
        elif other_side == LEFT:
            if (new_x - 1, new_y) in day_input and day_input[(new_x - 1, new_y)] != p:
                break
        elif other_side == UP:
            if (new_x, new_y - 1) in day_input and day_input[(new_x, new_y - 1)] != p:
                break
        elif other_side == DOWN:
            if (new_x, new_y + 1) in day_input and day_input[(new_x, new_y + 1)] != p:
                break

        visited.add((new_x, new_y, go_horizontal, side))
        line_coord_to_modify = (new_x, new_y)
    return line_coord_to_modify, visited


@timer(return_time=True)
def task2(day_input):
    plant_areas, plant_edges = analyze_areas(day_input)
    all_lines = []

    for plant_area, edges in zip(plant_areas, plant_edges):
        p = plant_area[0][2]
        area_lines = []
        visited = set()
        # just the coords around the plant area
        edge_coords = set((x, y) for x, y, _ in edges)

        # check every edge coord with the respective side from where it came
        for x, y, (dx, dy) in edges:
            # Side is important to know because there can be two "same" lines but with different sides (H in example)
            # XXOOXX
            # OOHHOO
            # XXOOXX
            side = RIGHT if dx == 1 else LEFT if dx == -1 else UP if dy == -1 else DOWN
            go_horizontal = (side == UP) or (side == DOWN)

            # Line was already calculated before because we visited this coord from this side already
            if (x, y, go_horizontal, side) in visited:
                continue
            # If now, then we need to calculate the line in the direction of the side
            visited.add((x, y, go_horizontal, side))

            # mark line start and end
            line_start = (x, y)
            line_end = (x, y)

            # check if we need to go left and right or up and down
            if go_horizontal:
                # first go left till we reach a coord that is not in the edge_coords
                # it could be a plant from this area or a field with the distance of 2 to the plant area

                # go left
                line_start, visited = walk_line(day_input, p, line_start, edge_coords, visited, go_horizontal, side, x, y, dx=-1)
                # go right
                line_end, visited = walk_line(day_input, p, line_end, edge_coords, visited, go_horizontal, side, x, y, dx=1)
            else:
                # go up
                line_start, visited = walk_line(day_input, p, line_start, edge_coords, visited, go_horizontal, side, x, y, dy=-1)
                # go down
                line_end, visited = walk_line(day_input, p, line_end, edge_coords, visited, go_horizontal, side, x, y, dy=1)

            area_lines.append((line_start, line_end))

        all_lines.append(area_lines)
    return sum(len(p) * len(lines) for p, lines in zip(plant_areas, all_lines))


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
