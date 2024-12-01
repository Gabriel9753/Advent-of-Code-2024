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


@timer(return_time=True)
def task1(day_input):
    day_input = day_input.splitlines()
    times = re.findall(r"(\d+)", day_input[0])
    times = [int(time) for time in times]
    distances = re.findall(r"\d+", day_input[1])
    distances = [int(dist) for dist in distances]

    result = 1
    f_acceleration = lambda t: t
    f_distance = lambda max_time, t: (max_time - t) * f_acceleration(t)

    for max_time, max_dist in zip(times, distances):
        new_records = 0
        for t in range(max_time+1):
            dist = f_distance(max_time, t)
            if dist > max_dist:
                new_records += 1
        result *= new_records
    return result

def calc_intersections(max_t, max_d):
    pre = max_t / 2
    discriminant = math.sqrt(pre**2 - max_d)
    return int(pre + discriminant), int(pre - discriminant)

@timer(return_time=True)
def task2(day_input):
    day_input = day_input.splitlines()
    times = re.findall(r"(\d+)", day_input[0])
    race_time = int("".join(times))
    distances = re.findall(r"\d+", day_input[1])
    race_dist = int("".join(distances))
    t1, t2 = calc_intersections(race_time, race_dist)
    return abs(t1 - t2)

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
    print(f"Task 1: {time_task1:.10f} seconds")
    print(f"Task 2: {time_task2:.10f} seconds")
    # Day 6
    # ------------------

    # Answers:
    # Task 1: 2269432
    # Task 2: 35865985

    # Times:
    # Task 1: 0.0000000000 seconds
    # Task 2: 0.0000000000 seconds

if __name__ == "__main__":
    main()
