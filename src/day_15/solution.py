import os
import re
import sys
from collections import deque
from datetime import datetime
import argparse
from copy import deepcopy

from rich import print

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")

DIRS = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

@timer(return_time=True)
def preprocess_input(input_data):
    # Preprocess the input data (if needed)
    input_data = input_data.split("\n\n")
    player_pos = None
    _map = {}
    for y, line in enumerate(input_data[0].split("\n")):
        for x, char in enumerate(line):
            if char == "@":
                player_pos = (x, y)
                _map[(x, y)] = "."
                continue
            _map[(x, y)] = char
    return (_map, player_pos, list(input_data[1].replace("\n", "")))


@timer(return_time=True)
def task1(day_input):
    _map, player_pos, instructions = day_input

    for instruction in instructions:
        cur_dir = DIRS[instruction]
        new_pos = (player_pos[0] + cur_dir[0], player_pos[1] + cur_dir[1])

        if _map[new_pos] == ".":
            player_pos = new_pos
            continue

        if _map[new_pos] == "#":
            continue

        if _map[new_pos] == "O":
            is_movable = False
            i = 1
            while True:
                new_box_pos = (new_pos[0] + i * cur_dir[0], new_pos[1] + i * cur_dir[1])
                if _map[new_box_pos] == "#":
                    break
                if _map[new_box_pos] == ".":
                    is_movable = True
                    break
                i += 1

            if is_movable:
                _map[new_pos], _map[new_box_pos], player_pos = ".", "O", new_pos

    gps_score = sum([100 * y + x for (x, y), v in _map.items() if v == "O"])
    return gps_score


@timer(return_time=True)
def task2(day_input):
    _map, player_pos, instructions = day_input
    # scale the x-axis of _map by 2 but keep y-axis the same
    scaled_map = {}
    for (x, y), v in _map.items():
        scaled_map[(2 * x, y)] = "[" if v == "O" else v
        scaled_map[(2 * x + 1, y)] = "]" if v == "O" else v
    player_pos = (2 * player_pos[0], player_pos[1])
    scaled_map[player_pos] = "@"

    for instruction in instructions:
        cur_dir = DIRS[instruction]
        new_pos = (player_pos[0] + cur_dir[0], player_pos[1] + cur_dir[1])

        if scaled_map[new_pos] == ".":
            scaled_map[player_pos] = "."
            scaled_map[new_pos] = "@"
            player_pos = new_pos
            continue

        if scaled_map[new_pos] == "#":
            continue

        if scaled_map[new_pos] in ("[", "]"):
            # if cur instruction is right or left, nothing special happens
            if instruction in ("<", ">"):
                last_pos = None
                i = 1
                while True:
                    new_box_pos = (new_pos[0] + i * cur_dir[0], new_pos[1] + i * cur_dir[1])
                    if scaled_map[new_box_pos] == "#":
                        break
                    if scaled_map[new_box_pos] == ".":
                        last_pos = new_box_pos
                        break
                    i += 1

                if last_pos:
                    scaled_map[player_pos] = "."
                    player_pos = new_pos

                    # move the boxes to left/right from the last_pos
                    alter_symbols = ["[", "]"] if instruction == "<" else ["]", "["]
                    back_dir = (-cur_dir[0], -cur_dir[1])
                    i = 0
                    cur_symbol = alter_symbols[i]
                    while True:
                        new_box_pos = (last_pos[0] + i * back_dir[0], last_pos[1] + i * back_dir[1])
                        scaled_map[new_box_pos] = cur_symbol
                        i += 1
                        cur_symbol = alter_symbols[i % 2]
                        if new_box_pos == new_pos:
                            scaled_map[new_pos] = "@"
                            break
            else:
                # now things get a bit complicated
                # check if all the boxes are movables to the up or down

                # 1. get all boxes affected by the instruction (so DIRECTLY in contact with the player or the box)
                # 2. check if any # occurs a top or bottom of the boxes
                # 3 (a). if no # occurs, move all the boxes up or down
                # 3 (b). if # occurs, no movement

                movable = True
                visited = set()
                queue = deque()
                if scaled_map[new_pos] == "[":
                    queue.extend([(new_pos, (new_pos[0] + 1, new_pos[1]))])
                else:
                    queue.extend([((new_pos[0] - 1, new_pos[1]), new_pos)])
                while queue:
                    cur_box = queue.popleft()

                    if cur_box in visited:
                        continue
                    visited.add(cur_box)

                    new_pos1 = (cur_box[0][0] + cur_dir[0], cur_box[0][1] + cur_dir[1])
                    new_pos2 = (cur_box[1][0] + cur_dir[0], cur_box[1][1] + cur_dir[1])

                    if scaled_map[new_pos1] == "#" or scaled_map[new_pos2] == "#":
                        movable = False
                        break

                    if scaled_map[new_pos1] == "." and scaled_map[new_pos2] == ".":
                        continue

                    if scaled_map[new_pos1] == "[" and scaled_map[new_pos2] == "]":
                        queue.extend([(new_pos1, new_pos2)])
                        continue

                    if scaled_map[new_pos1] == "]":
                        queue.extend([((new_pos1[0] - 1, new_pos1[1]), new_pos1)])

                    if scaled_map[new_pos2] == "[":
                        queue.extend([(new_pos2, (new_pos2[0] + 1, new_pos2[1]))])

                # go visited from the last to the first and move the box up or down
                if movable:
                    # sort the visited by y-axis (asc if instruction is up, desc if instruction is down)
                    visited = deque(sorted(visited, key=lambda x: x[0][1], reverse=instruction == "v"))

                    while visited:
                        cur_box = visited.popleft()
                        new_pos1 = (cur_box[0][0] + cur_dir[0], cur_box[0][1] + cur_dir[1])
                        new_pos2 = (cur_box[1][0] + cur_dir[0], cur_box[1][1] + cur_dir[1])

                        scaled_map[cur_box[0]] = "."
                        scaled_map[cur_box[1]] = "."
                        scaled_map[new_pos1] = "["
                        scaled_map[new_pos2] = "]"

                    scaled_map[new_pos] = "@"
                    scaled_map[player_pos] = "."
                    player_pos = new_pos

    gps_score = sum([100 * y + x for (x, y), v in scaled_map.items() if v == "["])
    return gps_score


def main(args):
    # Choose between the real input or the example input
    if args.example:
        day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    else:
        day_input = load_input(os.path.join(cur_dir, "input.txt"))

    day_input, t = preprocess_input(day_input)
    result_task1, time_task1 = task1(deepcopy(day_input))
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
