import math
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import load_input, timer

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day

available_colors = ["red", "green", "blue"]

max_colors = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def get_color_from_subset(subset):
    drawings = [draw.strip() for draw in subset.split(",")]
    colors = defaultdict(int)

    for drawing in drawings:
        for color in available_colors:
            if color in drawing:
                colors[color] += int(drawing.split(" ")[0])
                break

    return colors


@timer(return_time=True)
def task1(day_input):
    games = [game.split(": ")[-1] for game in day_input.split("\n")]
    subgames = [subgame for subgame in (game.split(";") for game in games)]

    possible_games = []
    for i, game in enumerate(games):
        is_game_possible = True
        for subset in subgames[i]:
            subset_colors = get_color_from_subset(subset)
            if any(value > max_colors[key] for key, value in subset_colors.items()):
                is_game_possible = False
                break
        if is_game_possible:
            possible_games.append(i + 1)

    return sum(possible_games)


@timer(return_time=True)
def task2(day_input):
    games = [game.split(": ")[-1] for game in day_input.split("\n")]
    subgames = [subgame for subgame in (game.split(";") for game in games)]
    powers = 0
    for i, game in enumerate(games):
        max_colors = defaultdict(int)
        for subset in subgames[i]:
            subset_colors = get_color_from_subset(subset)
            for key, value in subset_colors.items():
                if value > max_colors[key]:
                    max_colors[key] = value
        powers += math.prod(max_colors.values())

    return powers


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

    # Day 2
    # ------------------

    # Answers:
    # Task 1: 3059
    # Task 2: 65371

    # Times:
    # Task 1: 0.000999 seconds
    # Task 2: 0.000499 seconds


if __name__ == "__main__":
    main()
