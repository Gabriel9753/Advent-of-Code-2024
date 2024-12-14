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
from PIL import Image
from rich import print

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")
# day_img_dir = os.path.join(images_path, f"viz_{cur_day}")
# if not os.path.isdir(day_img_dir):
#     os.makedirs(day_img_dir)
# else:
#     for file in os.listdir(day_img_dir):
#         os.remove(os.path.join(day_img_dir, file))

# MAP_WIDTH = 11
MAP_WIDTH = 101
# MAP_HEIGHT = 7
MAP_HEIGHT = 103

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]


@timer(return_time=True)
def preprocess_input(input_data):
    return [list(map(int, re.findall(r"\-?\d+", x))) for x in input_data.splitlines()]


def new_pos(x, y, dx, dy, t):
    return ((x + (t * dx)) % MAP_WIDTH, (y + (t * dy)) % MAP_HEIGHT)


@timer(return_time=True)
def task1(day_input):
    processed = [new_pos(x, y, dx, dy, 100) for x, y, dx, dy in day_input]
    # count all robots in each quadrant:
    q1 = q2 = q3 = q4 = 0
    mid_x, mid_y = MAP_WIDTH // 2, MAP_HEIGHT // 2

    for x, y in processed:
        if x < mid_x and y < mid_y:
            q1 += 1
        if x > mid_x and y < mid_y:
            q2 += 1
        if x < mid_x and y > mid_y:
            q3 += 1
        if x > mid_x and y > mid_y:
            q4 += 1

    return q1 * q2 * q3 * q4


###################################
#### Old solution for rendering ###
###################################
# def render(coords, colors, t):
#     if t % 6888 != 0 or t == 0:
#         return
#     np_img = np.zeros((MAP_HEIGHT, MAP_WIDTH, 3), dtype=np.uint8)
#     for i, (x, y) in enumerate(coords):
#         np_img[y, x] = [*colors[i]]
#     np_img = np.repeat(np_img, 8, axis=0)
#     np_img = np.repeat(np_img, 8, axis=1)

#     img = Image.fromarray(np_img)
#     img.save(os.path.join(day_img_dir, f"viz_{t:05d}.png"), "PNG")


@timer(return_time=True)
def task2(day_input):
    # global TIME_STEPS
    robots_with_max_neighbors = []
    # robot_colors = np.random.randint(0, 255, (len(day_input), 3))
    max_time = 7_000  # set higher if not known

    for t in range(max_time):
        ###################################
        #### Old solution for rendering ###
        ###################################
        # pos_to_render = [new_pos(x, y, dx, dy) for x, y, dx, dy in day_input]
        # render(pos_to_render, robot_colors)

        robots = {new_pos(x, y, dx, dy, t) for x, y, dx, dy in day_input}
        max_neighbors = sum(all((r[0] + dx, r[1] + dy) in robots for dx, dy in DIRS) for r in robots)
        robots_with_max_neighbors.append((t, max_neighbors))

    max_time, max_neighbors = max(robots_with_max_neighbors, key=lambda x: x[1])
    return max_time


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
