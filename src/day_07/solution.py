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

from enum import Enum

card_value = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "1": 1,
}


class Strength(Enum):
    FIVE = 7
    FOUR = 6
    FULL_HOUSE = 5
    THREE = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


joker = "J"


def get_normal_hand_value(hand):
    _value = 0
    for i, c in zip(range(len(hand), 0, -1), hand):
        _value += card_value[c] * 100**i
    return _value


def rank_hand(hand):
    # return a rank based on the hand
    cards = [c for c in hand]
    counts = Counter(cards)
    if any(v == 5 for v in counts.values()):
        return Strength.FIVE.value
    elif any(v == 4 for v in counts.values()):
        return Strength.FOUR.value
    elif any(v == 3 for v in counts.values()) and any(v == 2 for v in counts.values()):
        return Strength.FULL_HOUSE.value
    elif any(v == 3 for v in counts.values()):
        return Strength.THREE.value
    elif len([v for v in counts.values() if v == 2]) == 2:
        return Strength.TWO_PAIRS.value
    elif any(v == 2 for v in counts.values()):
        return Strength.ONE_PAIR.value
    else:
        return Strength.HIGH_CARD.value


def improve_hand(hand):
    hand, v, cur_rank = hand
    if joker not in hand:
        return [hand, v, cur_rank]
    hand_copy = hand
    counts = Counter([c for c in hand])

    if cur_rank == Strength.TWO_PAIRS.value:
        pairs = [k for k, v in counts.items() if v == 2]
        hand = hand.replace(joker, max(pairs, key=card_value.get))
    elif cur_rank == Strength.HIGH_CARD.value:
        highest_card = max([c for c in hand if c != joker], key=card_value.get)
        hand = hand.replace(joker, highest_card)
    elif cur_rank == Strength.ONE_PAIR.value:
        pair = [k for k, v in counts.items() if v == 2][0]
        highest_card_except_pair = max(
            [c for c in hand if c != pair], key=card_value.get
        )
        hand = (
            hand.replace(joker, pair)
            if pair != joker
            else hand.replace(joker, highest_card_except_pair)
        )
    elif cur_rank == Strength.THREE.value:
        triple = [k for k, v in counts.items() if v == 3][0]
        if triple == joker:
            highest_card_except_triple = max(
                [c for c in hand if c != triple], key=card_value.get
            )
            hand = hand.replace(joker, highest_card_except_triple)
        else:
            hand = hand.replace(joker, triple)
    elif cur_rank == Strength.FOUR.value:
        four = [k for k, v in counts.items() if v == 4][0]
        if four == joker:
            highest_card_except_four = max(
                [c for c in hand if c != four], key=card_value.get
            )
            hand = hand.replace(joker, highest_card_except_four)
        else:
            hand = hand.replace(joker, four)
    elif cur_rank == Strength.FIVE.value:
        hand = hand.replace(joker, "A")
    elif cur_rank == Strength.FULL_HOUSE.value:
        triple = [k for k, v in counts.items() if v == 3][0]
        pair = [k for k, v in counts.items() if v == 2][0]
        if triple == joker:
            hand = hand.replace(joker, pair)
        else:
            hand = hand.replace(joker, triple)

    return [hand_copy, v, rank_hand(hand)]


@timer(return_time=True)
def task1(day_input):
    day_input = day_input.splitlines()
    hands = [line.split() for line in day_input]
    hands = [[hand[0], int(hand[1]), rank_hand(hand[0])] for hand in hands]
    hands = sorted(hands, key=lambda x: x[2], reverse=True)

    ranked_hands = defaultdict(list)
    for hand in hands:
        ranked_hands[hand[2]].append(hand)

    for key, value in ranked_hands.items():
        ranked_hands[key] = sorted(
            value, key=lambda x: get_normal_hand_value(x[0]), reverse=True
        )

    hands = []
    for key, value in ranked_hands.items():
        hands.extend(value)

    result = 0
    for rank, hand in enumerate(hands[::-1], 1):
        result += rank * hand[1]
    return result


@timer(return_time=True)
def task2(day_input):
    global card_value
    card_value[joker] = 0
    day_input = day_input.splitlines()
    hands = [line.split() for line in day_input]
    hands = [[hand[0], int(hand[1]), rank_hand(hand[0])] for hand in hands]
    hands = [improve_hand(hand) for hand in hands]

    hands = sorted(hands, key=lambda x: x[2], reverse=True)

    # if the rank is the same, then compare the value of the hand with get_normal_hand_value function
    ranked_hands = defaultdict(list)
    for hand in hands:
        ranked_hands[hand[2]].append(hand)

    for key, value in ranked_hands.items():
        ranked_hands[key] = sorted(
            value, key=lambda x: get_normal_hand_value(x[0]), reverse=True
        )

    hands = []
    for key, value in ranked_hands.items():
        hands.extend(value)

    result = 0
    for rank, hand in enumerate(hands[::-1], 1):
        result += rank * hand[1]
    return result


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
    print(f"Task 1: {time_task1:.6f} seconds")
    print(f"Task 2: {time_task2:.6f} seconds")

    # Day 7
    # ------------------

    # Answers:
    # Task 1: 250946742
    # Task 2: 251824095

    # Times:
    # Task 1: 0.005032 seconds
    # Task 2: 0.006004 seconds


if __name__ == "__main__":
    main()
