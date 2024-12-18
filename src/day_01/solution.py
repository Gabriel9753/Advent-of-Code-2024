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

from util.general_util import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")


def split_in_two_list(day_input):
    # iter for all elements in the list and find the first and second number (with re) (convert to int)
    first = [int(re.findall(r"\d+", i)[0]) for i in day_input]
    second = [int(re.findall(r"\d+", i)[1]) for i in day_input]
    return first, second


@timer(return_time=True)
def task1(day_input):
    # Day-specific code for Task 1
    left, right = day_input
    left.sort()
    right.sort()

    return sum(np.abs(np.array(left) - np.array(right)))


@timer(return_time=True)
def task2(day_input):
    # Day-specific code for Task 2
    left, right = day_input

    # count all unique elements in the left and right list
    left_count = Counter(left)
    right_count = Counter(right)

    result = sum([count * num * right_count[num] for num, count in left_count.items()])

    return result


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt"))
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt"))

    day_input = split_in_two_list(day_input.split("\n"))

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

    # 1000 times and average the time
    avg_time_task1 = average_time(1000, task1, day_input)
    avg_time_task2 = average_time(1000, task2, day_input)
    print("\nAverage times:")
    print(f"Task 1: {avg_time_task1:.6f} seconds")
    print(f"Task 2: {avg_time_task2:.6f} seconds")
    write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    main()
