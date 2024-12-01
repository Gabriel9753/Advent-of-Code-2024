import os
import re
import sys
import time

cur_dir = os.path.dirname(os.path.abspath(__file__))
# full path to the parent directory
readme_dir = os.path.dirname(os.path.dirname(cur_dir))
README_PATH = os.path.join(readme_dir, "README.md")


# Timer decorator to measure the execution time of a function
def timer(return_time=False):
    """
    Example usage:
    @timer(return_time=True)\\
    def example_function():
        # Your code here
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            if return_time:
                return result, execution_time
            else:
                print(f"{func.__name__}: {execution_time:.6f} seconds")
                return result

        return wrapper

    return decorator


def load_input(input_file_path):
    try:
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            return input_file.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file not found ({input_file_path})")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading input {input_file_path}: {e}")
        sys.exit(1)


def average_time(runs, func, *args, **kwargs):
    total_time = 0
    for _ in range(runs):
        _, time = func(*args, **kwargs)
        total_time += time
    return total_time / runs


def write_times_to_readme(day, time_task1, time_task2):
    if not os.path.exists(README_PATH):
        print(f"Error: README file not found ({README_PATH})")
        sys.exit(1)

    with open(README_PATH, "r") as file:
        lines = file.readlines()

    updated = False
    for i, line in enumerate(lines):
        # Match the line corresponding to the specific day in the table
        match = re.match(rf"^\| {day} +\| +([\d.-]+|-) +\| +([\d.-]+|-) +\|$", line)
        if match:
            # Replace the old times with the new ones
            lines[i] = f"| {day}   | {time_task1:.6f}      | {time_task2:.6f}      |\n"
            updated = True
            break

    if not updated:
        print(f"Error: Day {day} not found in the table.")
        sys.exit(1)

    with open(README_PATH, "w") as file:
        file.writelines(lines)

    print(f"Times for Day {day} updated successfully.")
