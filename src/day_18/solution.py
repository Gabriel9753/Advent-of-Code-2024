import math
import os
import re
import sys
from collections import deque
from datetime import datetime
import argparse

from rich import print

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")

# WIDTH, HEIGHT = 7, 7
WIDTH, HEIGHT = 71, 71
T = 12

@timer(return_time=True)
def preprocess_input(input_data):
    return [list(map(int, re.findall(r"\d+", line))) for line in input_data.splitlines()]

def get_mem_space():
    _map = {(x, y): "." for x in range(WIDTH) for y in range(HEIGHT)}
    _map[(0, 0)] = "S"
    _map[(WIDTH-1, HEIGHT-1)] = "E"
    return _map

def get_neighbours(x, y):
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]


class CustomCache:
    def __init__(self, num_args):
        self.num_args = num_args
        self.cache = {}

    def __call__(self, func):
        def wrapper(*args):
            relevant_args = args[:self.num_args]
            if relevant_args not in self.cache:
                self.cache[relevant_args] = func(*args)
            return self.cache[relevant_args]
        return wrapper

@CustomCache(num_args=1)
def get_map_t(t, mem_space, _bytes):
    for idx, (x, y) in zip(range(t), _bytes):
        mem_space[(x, y)] = "#"
    return mem_space



def get_path(mem_space_t):
    queue = deque([(0, 0, 0, [])])
    visited = set()
    shortest = math.inf
    shortest_path = []

    while queue:
        x, y, t, path = queue.popleft()

        if t >= shortest:
            continue

        if (x, y) in visited:
            continue
        visited.add((x, y))

        if mem_space_t[(x, y)] == "E":
            shortest = t
            shortest_path = path
            continue

        for nx, ny in get_neighbours(x, y):
            if (nx, ny) in mem_space_t and mem_space_t[(nx, ny)] != "#":
                queue.append((nx, ny, t+1, path + [(nx, ny)]))

    return shortest, set(shortest_path)



@timer(return_time=True)
def task1(day_input):
    _bytes = day_input
    mem_space_t = get_map_t(T, get_mem_space(), _bytes)
    return get_path(mem_space_t)[0]


@timer(return_time=True)
def task2(day_input):
    _bytes = day_input
    t = 0
    last_added = None
    while True:
        mem_space_t = get_map_t(t+1, get_mem_space(), _bytes)
        shortest, path = get_path(mem_space_t)
        if shortest == math.inf:
            break

        # go through the bytes and pick the time_step with a byte coordinate that is in the path
        for new_t, (x, y) in enumerate(_bytes[t+1:], start=t+1):
            if (x, y) in path:
                t = new_t
                last_added = (x, y)
                break

    return f"{last_added[0]},{last_added[1]}"



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
