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
    points = 0
    for line in day_input.splitlines():
        matches = re.findall(r"(.+):\s*((?:\d+\s+)+)\|\s*((?:\d+\s*)+)", line)
        winning_cards = [int(n) for n in matches[0][1].split()]
        played_cards = [int(n) for n in matches[0][2].split()]
        inter = list(set(winning_cards) & set(played_cards))
        points += 2 ** (len(inter) - 1) if len(inter) > 2 else len(inter)
    return points


@timer(return_time=True)
def task2(day_input):
    games = dict()
    for game_id, line in enumerate(day_input.splitlines(), 1):
        matches = re.findall(r"(.+):\s*((?:\d+\s+)+)\|\s*((?:\d+\s*)+)", line)
        winning_cards = [int(n) for n in matches[0][1].split()]
        played_cards = [int(n) for n in matches[0][2].split()]
        inter = list(set(winning_cards) & set(played_cards))
        games[game_id] = len(inter)

    scratchcards = 0
    # [wins, copies]
    cards = [[wins, 0] for wins in games.values()]
    for i, card in enumerate(cards):
        for j in range(i + 1, i + 1 + card[0]):
            cards[j][1] += card[1] + 1
        scratchcards += 1 + card[1]
    return scratchcards


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt"))
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt"))

    # Call the tasks and store their results (if needed)
    result_task1, time_task1 = task1(day_input)
    result_task2, time_task2 = task2(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    print("\nAnswers:")
    print(f"Task 1: {result_task1}")
    print(f"Task 2: {result_task2}")

    print("\nTimes:")
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")

    # Day 4
    # ------------------

    # Answers:
    # Task 1: 21919
    # Task 2: 9881048

    # Times:
    # Task 1: 0.001501 seconds
    # Task 2: 0.001532 seconds


if __name__ == "__main__":
    main()
