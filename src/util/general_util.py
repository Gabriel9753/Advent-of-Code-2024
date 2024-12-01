import sys
import time


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
