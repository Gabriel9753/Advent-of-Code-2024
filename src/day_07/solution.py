import os
import re
import sys
from datetime import datetime
from tqdm import tqdm

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import load_input, timer, average_time, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")


def check_recursively(desired_output, current_result, rv):
    global OPERATORS

    if len(rv) == 0:
        return current_result == desired_output

    v = rv[0]
    for operator in OPERATORS:
        new_result = operator(current_result, v)
        if new_result > desired_output:
            continue
        if check_recursively(desired_output, new_result, rv[1:]):
            return True

    return False


@timer(return_time=True)
def task1(day_input):
    global OPERATORS
    total_calibration = 0
    operators = [lambda x, y: x + y, lambda x, y: x * y]
    OPERATORS = operators
    for eq in day_input:
        # Start with the first number in the list and recursively check
        if check_recursively(eq[0], eq[1], eq[2:]):
            total_calibration += eq[0]
    return total_calibration


@timer(return_time=True)
def task2(day_input):
    global OPERATORS
    operators = [
        lambda x, y: int(str(x) + str(y)),
        lambda x, y: x * y,
        lambda x, y: x + y,
    ]
    OPERATORS = operators
    total_calibration = 0
    for eq in day_input:
        # Start with the first number in the list and recursively check
        if check_recursively(eq[0], eq[1], eq[2:]):
            total_calibration += eq[0]
    return total_calibration


def main():
    # Choose between the real input or the example input
    day_input = load_input(os.path.join(cur_dir, "input.txt"))
    # day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    day_input = [
        (int(line.split(": ")[0]), *map(int, line.split(": ")[1].split())) for line in tqdm(day_input.splitlines())
    ]

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

    # 100 times and average the time
    avg_time_task1 = average_time(10, task1, day_input)
    avg_time_task2 = average_time(10, task2, day_input)
    print("\nAverage times:")
    print(f"Task 1: {avg_time_task1:.6f} seconds")
    print(f"Task 2: {avg_time_task2:.6f} seconds")
    write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    main()
