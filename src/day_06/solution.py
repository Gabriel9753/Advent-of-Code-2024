import math
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict, deque, namedtuple
from datetime import datetime
from copy import deepcopy
from functools import lru_cache, reduce
from itertools import chain, combinations, permutations, product

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

UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)
DIR_CYCLE = [UP, RIGHT, DOWN, LEFT]


def is_outside(np_grid, pos):
    return not (0 <= pos[0] < np_grid.shape[0] and 0 <= pos[1] < np_grid.shape[1])

def find_path(np_grid, obstacles, cur_pos, cur_direction):

    while True:
        x, y = cur_pos
        dir_x, dir_y = DIR_CYCLE[cur_direction]
        is_break_out = True
        while not is_outside(np_grid, (x, y)):
            if (x, y) in obstacles:
                is_break_out = False
                break
            # yield the position and direction for tracking the guard's path
            yield (x, y), cur_direction
            x += dir_x
            y += dir_y
        if is_break_out:
            break

        cur_pos = (x - dir_x, y - dir_y)
        cur_direction = (cur_direction + 1) % 4


@timer(return_time=True)
def task1(day_input):
    np_grid, obstacles, cur_pos, cur_direction = day_input
    return len({(pos) for pos, _ in find_path(np_grid, obstacles, cur_pos, cur_direction)})



@timer(return_time=True)
def task2(day_input):
    np_grid, obstacles, cur_pos, cur_direction = day_input
    start_pos = cur_pos
    visited = set(find_path(np_grid, obstacles, cur_pos, cur_direction))

    new_obstacle_positions = set()
    # on the full path, check every position and direction for a potential new obstacle to create a loop
    for pos, direction in tqdm(visited, desc="Checking for new obstacles"):
        x, y = pos
        dir_x, dir_y = DIR_CYCLE[direction]

        new_obstacle_position = (x + dir_x, y + dir_y)

        # check if the new obstacle is valid
        if (
            is_outside(np_grid, new_obstacle_position)
            or new_obstacle_position in obstacles
            or new_obstacle_position in new_obstacle_positions
            or new_obstacle_position == start_pos
        ):
            continue

        # Start from begin and check if the new obstacle will create a loop
        temp_obstacles = obstacles | {new_obstacle_position}
        cur_pos = start_pos
        cur_direction = 0
        visited_states = set()

        while True:
            state = (cur_pos, cur_direction)
            if state in visited_states:
                # if golem was already at this position and direction, then there is a loop, add the new obstacle
                new_obstacle_positions.add(new_obstacle_position)
                break
            visited_states.add(state)

            x, y = cur_pos
            dir_x, dir_y = DIR_CYCLE[cur_direction]
            next_pos = (x + dir_x, y + dir_y)

            # breaking the loop!
            if is_outside(np_grid, next_pos):
                break

            # check if direction needs to be changed because of obstacle
            if next_pos in temp_obstacles:
                cur_direction = (cur_direction + 1) % 4
            else:
                # just update the position if there is no obstacle
                cur_pos = next_pos

    return len(new_obstacle_positions)


def main():
    day_input = load_input(os.path.join(cur_dir, "input.txt"))
    np_grid = np.array([list(row) for row in day_input.split("\n")])
    obstacles = set()
    cur_pos, cur_direction = (0, 0), DIR_CYCLE.index(UP)

    for i, row in enumerate(np_grid):
        for j, char in enumerate(row):
            if char == "#":
                obstacles.add((i, j))
            elif char == "^":
                cur_pos = (i, j)

    day_input = (np_grid, obstacles, cur_pos, cur_direction)
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

    # 100 times and average the time
    avg_time_task1 = average_time(10, task1, day_input)
    avg_time_task2 = average_time(10, task2, day_input)
    print("\nAverage times:")
    print(f"Task 1: {avg_time_task1:.6f} seconds")
    print(f"Task 2: {avg_time_task2:.6f} seconds")
    write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    main()
