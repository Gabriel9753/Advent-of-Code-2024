import math
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict, deque, namedtuple
from datetime import datetime
from functools import lru_cache, reduce
from itertools import chain, combinations, permutations, product

import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import convolve2d
from tqdm import tqdm

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import load_input, timer

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day

# get all string symbols that are not digits or truncation symbols
symbols = [chr(i) for i in range(128)]
symbols = [c for c in symbols if not c.isdigit() and c != "."]

max_neighbors = 2


def plot_masks(before_, after_):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    ax1.imshow(before_, cmap="gray")
    ax2.imshow(after_, cmap="gray")
    plt.suptitle("Input mask before and after convolution")
    ax1.axis("off")
    ax2.axis("off")
    plt.tight_layout()
    save_dir = os.path.join(par_dir, "images")
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f"day_{cur_day}_input_mask.png"))
    plt.close()


@timer(return_time=True)
def task1(day_input, do_plot=False):
    """
    Task 1 was solved by using a convolution mask to find the symbols that are neighbors of the symbols.
    """
    lines = day_input.split("\n")

    input_mask = np.array([[1 if c in symbols else 0 for c in line] for line in lines])
    # create a 2D image for the input mask before and after convolution
    before_ = input_mask.copy()
    input_mask = (convolve2d(input_mask, np.ones((3, 3)), mode="same") > 0).astype(int)
    after_ = input_mask.copy()
    if do_plot:
        plot_masks(before_, after_)

    sum_ = 0
    for i, line in enumerate(lines):
        if any(c.isdigit() for c in line):
            digits = [(int(m.group()), m.start()) for m in re.finditer(r"\d+", line)]
            for num, start_idx in digits:
                num_range = range(start_idx, start_idx + len(str(num)))
                if any(input_mask[i, idx] == 1 for idx in num_range):
                    sum_ += num
    return sum_


@timer(return_time=True)
def task2(day_input):
    """
    Task 2 was solved checking all '*' symbols and finding all the numbers that are neighbors of the '*' symbols.
    If the number of neighbors is equal to the max_neighbors, then the product of the numbers is added to the sum.
    """
    lines = day_input.split("\n")
    check_directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    ]
    dirs = lambda x, y: [(x + dx, y + dy) for dx, dy in check_directions]
    sum_ = 0

    target_symbols = [
        (m.group(), m.start(), y)
        for y, line in enumerate(lines)
        for m in re.finditer(r"\*+", line)
    ]
    target_numbers = [
        (m.group(), range(m.start(), m.end()), y)
        for y, line in enumerate(lines)
        for m in re.finditer(r"\d+", line)
    ]

    for _, start_idx, y in target_symbols:
        neighbors = set()
        for x_, y_ in dirs(start_idx, y):
            target_numbers_ = [p for p in target_numbers if p[2] == y_ and x_ in p[1]]
            neighbors.update(target_numbers_)
        if len(neighbors) == max_neighbors:
            sum_ += math.prod([int(n[0]) for n in neighbors])
    return sum_


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt"))
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt"))

    # Call the tasks and store their results (if needed)
    result_task1, time_task1 = task1(day_input, do_plot=False)
    result_task2, time_task2 = task2(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    print("\nAnswers:")
    print(f"Task 1: {result_task1}")
    print(f"Task 2: {result_task2}")

    print("\nTimes:")
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")

    # Day 3
    # ------------------

    # Answers:
    # Task 1: 522726
    # Task 2: 81721933

    # Times:
    # Task 1: 0.018015 seconds
    # Task 2: 0.054046 seconds


if __name__ == "__main__":
    main()
