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


class CategoryMap:
    def __init__(self, category, target_category, lists):
        self.category = category
        self.target_category = target_category
        # each list: [destination range start, source range start, range length]
        self._maps = [((l[0], l[0] + l[2] - 1), (l[1], l[1] + l[2] - 1)) for l in lists]

    def get_most_promising_map(self, range):
        best_map = None
        best_map_score = -np.inf
        for _map in self._maps:
            score = min(range[1], _map[1][1]) - max(range[0], _map[1][0])
            if score > best_map_score:
                best_map = _map
                best_map_score = score
        return best_map

    def map_ranges(self, ranges):
        new_ranges = []
        for r in ranges:
            _map = self.get_most_promising_map(r)
            # all before source range
            if r[1] < _map[1][0]:
                new_ranges.append((r[0], r[1], 1))
            # all after source range
            elif r[0] > _map[1][1]:
                new_ranges.append((r[0], r[1], 1))
            # some seeds before source range, some seeds in source range
            elif r[0] < _map[1][0] and r[1] >= _map[1][0] and r[1] <= _map[1][1]:
                range_before = (r[0], _map[1][0] - 1, 0)
                in_numbers = r[1] - _map[1][0]
                range_in = (_map[0][0], _map[0][0] + in_numbers, 1)
                new_ranges.append(range_before)
                new_ranges.append(range_in)
            # some seeds before source range, some seeds in source range, some seeds after source range
            elif r[0] < _map[1][0] and r[1] > _map[1][1]:
                range_before = (r[0], _map[1][0] - 1, 0)
                in_numbers = _map[1][1] - _map[1][0] + 1
                range_in = (_map[0][0], _map[0][0] + in_numbers, 1)
                range_after = (_map[0][1] + 1, r[1], 0)
                new_ranges.append(range_before)
                new_ranges.append(range_in)
                new_ranges.append(range_after)
            # some seeds in source range, some seeds after source range
            elif r[0] >= _map[1][0] and r[1] > _map[1][1]:
                start = _map[0][0] + (r[0] - _map[1][0])
                range_in = (start, _map[0][1], 1)
                range_after = (_map[1][1] + 1, r[1], 0)
                new_ranges.append(range_in)
                new_ranges.append(range_after)
            # all in source range
            elif r[0] >= _map[1][0] and r[1] <= _map[1][1]:
                start = _map[0][0] + (r[0] - _map[1][0])
                end = start + (r[1] - r[0])
                new_ranges.append((start, end, 1))
            # all after source range
            elif r[0] > _map[1][1]:
                new_ranges.append((r[0], r[1], 1))
            else:
                print("something went wrong")
                break
        return new_ranges

    def process_ranges(self, ranges):
        finished = []
        all_processed = False
        while not all_processed:
            before_ranges = ranges.copy()
            new_ranges = self.map_ranges(ranges)
            finished.extend([r for r in new_ranges if r[2] == 1])
            ranges = [r for r in new_ranges if r[2] == 0]
            if len(ranges) == 0:
                all_processed = True
            elif before_ranges == ranges:
                print("no progress")
                break

        # print(f"new ranges: {finished}")
        return finished

    def _map(self, value):
        for dest_range, source_range in self._maps:
            if source_range[0] <= value <= source_range[1]:
                return dest_range[0] + value - source_range[0]
        return value


def build_category_maps(day_input):
    category_maps = {}
    for match in re.finditer(
        r"(\w+)-to-(\w+) map:\n([\d\s]+\n)+", day_input, re.MULTILINE
    ):
        category, target_category, number_lists = match.groups()
        lists = [
            list(map(int, lst.split())) for lst in number_lists.strip().split("\n")
        ]
        category_maps[category] = CategoryMap(category, target_category, lists)
    return category_maps


@timer(return_time=True)
def task1(day_input):
    seeds = re.findall(r"seeds: ([\d\s]+)", day_input)[0].split()
    category_maps = build_category_maps(day_input)
    dest_values = list()
    for seed in seeds:
        for category, category_map in category_maps.items():
            seed = category_map._map(int(seed))
        dest_values.append(seed)
    return min(dest_values)


@timer(return_time=True)
def task2(day_input):
    s = [int(s) for s in re.findall(r"seeds: ([\d\s]+)", day_input)[0].split()]
    # each 'seed' stores the start and end of a range, and whether it was mapped or not
    seeds = [(s[i], s[i] + s[i + 1] - 1, 0) for i in range(0, len(s), 2)]
    seeds = sorted(seeds, key=lambda x: x[0])
    category_maps = build_category_maps(day_input)
    processed_seeds = seeds.copy()
    for _, category_map in category_maps.items():
        processed_seeds = category_map.process_ranges(processed_seeds)
    processed_seeds = sorted(processed_seeds, key=lambda x: x[0])
    return min([s[0] for s in processed_seeds if s[0] != 0])


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt"))
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt"))

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
    # Day 5
    # ------------------

    # Answers:
    # Task 1: 551761867
    # Task 2: 57451709

    # Times:
    # Task 1: 0.000000 seconds
    # Task 2: 0.006023 seconds


if __name__ == "__main__":
    main()
