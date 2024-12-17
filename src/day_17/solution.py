import os
import re
import sys
from collections import deque
from datetime import datetime
import argparse

from rich import print

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")

"""
The computer operates as a 3-bit register-based system, capable of storing values between 0 and 7.
The program consists of pairs of values:
- Even indices contain instructions.
- Odd indices contain operands.

Operands are divided into two types:
1. Literal Operands (lop): Represent explicit numerical values.
2. Combo Operands (cop): Represent specific values based on their range:
   - 0–3: Actual values 0–3.
   - 4: Value stored in Register A.
   - 5: Value stored in Register B.
   - 6: Value stored in Register C.
   - 7: Invalid operand.

The insturction pointer starts at 0 and increments by 2 after each instruction unless a jump is executed.

Instructions:
    - 0 (adv): divison. A = int(A / 2^cop)
    - 1 (bxl): bitwise XOR. B = B XOR lop
    - 2 (bst): B = cop % 8
    - 3 (jnz): Nothin if A == 0, else jump to lop (not increase normal by 2 if jump)
    - 4 (bxc): B = B XOR C
    - 5 (out): cop % 8
    - 6 (bdv): B = int(A / 2^cop)
    - 7 (cdv): C = int(A / 2^cop)
"""


class Computer:
    def __init__(self, program, registers):
        self.program = program
        self.registers = registers
        self.ip = 0
        self.output = []
        self.instruction_ptr = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def run(self):
        while 0 <= self.ip < len(self.program) - 1:
            self.execute_instruction()

    def execute_instruction(self):
        # Get the instruction and the operand
        instruction = self.program[self.ip]
        operand = self.program[self.ip + 1]

        # Execute the instruction
        self.ip = self.instruction_ptr[instruction](operand)

    def get_cop_value(self, operand):
        if operand < 4:
            return operand
        elif operand == 4:
            return self.registers["A"]
        elif operand == 5:
            return self.registers["B"]
        elif operand == 6:
            return self.registers["C"]
        else:
            return -1

    def adv(self, operand):
        self.registers["A"] //= 2 ** self.get_cop_value(operand)
        return self.ip + 2

    def bxl(self, operand):
        self.registers["B"] ^= operand
        return self.ip + 2

    def bst(self, operand):
        self.registers["B"] = self.get_cop_value(operand) % 8
        return self.ip + 2

    def jnz(self, operand):
        return operand if self.registers["A"] != 0 else self.ip + 2

    def bxc(self, operand):
        self.registers["B"] ^= self.registers["C"]
        return self.ip + 2

    def out(self, operand):
        self.output.append(self.get_cop_value(operand) % 8)
        return self.ip + 2

    def bdv(self, operand):
        self.registers["B"] = self.registers["A"] // 2 ** self.get_cop_value(operand)
        return self.ip + 2

    def cdv(self, operand):
        self.registers["C"] = self.registers["A"] // 2 ** self.get_cop_value(operand)
        return self.ip + 2

    def get_output(self):
        return ",".join(map(str, self.output))

    def get_list_output(self):
        return self.output


@timer(return_time=True)
def preprocess_input(input_data):
    # Preprocess the input data (if needed)
    input_data = input_data.splitlines()
    registers = {
        "A": int(re.findall(r"\d+", input_data[0])[0]),
        "B": int(re.findall(r"\d+", input_data[1])[0]),
        "C": int(re.findall(r"\d+", input_data[2])[0]),
    }
    program = [int(d) for d in re.findall(r"\d+", input_data[-1])]

    return (registers, program)


@timer(return_time=True)
def task1(day_input):
    computer = Computer(day_input[1], day_input[0])
    computer.run()
    return computer.get_output()


@timer(return_time=True)
def task2(day_input):
    registers, program = day_input
    candidates = deque([0])
    min_candidates = 2 ** (3 * (len(program) - 1))

    while candidates and candidates[-1] < min_candidates:
        seed = candidates.popleft()

        # iterate over all possible 6-bit values (0 to 2^6 - 1)
        for a in range(2**6):
            # combine the seed with the current 6-bit value
            a += seed << 6

            registers["A"] = a
            computer = Computer(program, registers)
            computer.run()
            out = computer.get_list_output()

            # small "A" values are padded with a leading 0
            if a < 8:
                out.insert(0, 0)

            # check if the generated output matches the last portion of the program
            # if true the current candidate "a" is added to the queue for further checks
            if out == program[-(len(out)) :]:
                candidates.append(a)

            # solution found
            if out == program:
                break

    return candidates.pop()


def main(args):
    # Choose between the real input or the example input
    if args.example:
        day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    else:
        day_input = load_input(os.path.join(cur_dir, "input.txt"))

    day_input, t = preprocess_input(day_input)
    result_task1, time_task1 = task1(day_input)
    result_task2, time_task2 = task2(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    print(f"Processing data: {t:.6f} seconds")
    print(f"Task 1: {result_task1} ({time_task1:.6f} seconds)")
    print(f"Task 2: {result_task2} ({time_task2:.6f} seconds)")

    if args.timeit:
        avg_time_task1 = average_time(100, task1, day_input)
        avg_time_task2 = average_time(100, task2, day_input)
        print("\nAverage times:")
        print(f"Task 1: {avg_time_task1:.6f} seconds")
        print(f"Task 2: {avg_time_task2:.6f} seconds")
        write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", type=int, help="Use the example input", default=1)
    parser.add_argument("--timeit", type=int, help="Average the execution time over 100 runs", default=0)
    main(parser.parse_args())
