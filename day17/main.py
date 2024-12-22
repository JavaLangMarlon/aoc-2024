import re

num_regex = re.compile(r'\d+')


def parse_input(path: str) -> tuple[list[int], int, int, int]:
    with (open(path) as f):
        lines = f.readlines()

        return (
            [int(num) for num in num_regex.findall(lines[4])],
            int(num_regex.findall(lines[0])[0]),
            int(num_regex.findall(lines[1])[0]),
            int(num_regex.findall(lines[2])[0])
        )


def get_combo_operand(operand: int, register_a: int, register_b: int, register_c: int) -> int:
    if operand < 4:
        return operand
    if operand == 4:
        return register_a
    if operand == 5:
        return register_b
    return register_c


def run_program(instructions: list[int], register_a: int, register_b: int, register_c: int) -> str:
    output = ""

    pc = 0
    while pc < len(instructions):
        if instructions[pc] == 0:
            register_a = register_a // 2 ** get_combo_operand(instructions[pc + 1], register_a, register_b, register_c)
            pc += 2
        elif instructions[pc] == 1:
            register_b = register_b ^ instructions[pc + 1]
            pc += 2
        elif instructions[pc] == 2:
            register_b = get_combo_operand(instructions[pc + 1], register_a, register_b, register_c) % 8
            pc += 2
        elif instructions[pc] == 3:
            pc = instructions[pc + 1] if register_a != 0 else pc + 2
        elif instructions[pc] == 4:
            register_b = register_b ^ register_c
            pc += 2
        elif instructions[pc] == 5:
            output += str(get_combo_operand(instructions[pc + 1], register_a, register_b, register_c) % 8) + ","
            pc += 2
        elif instructions[pc] == 6:
            register_b = register_a // 2 ** get_combo_operand(instructions[pc + 1], register_a, register_b, register_c)
            pc += 2
        else:
            register_c = register_a // 2 ** get_combo_operand(instructions[pc + 1], register_a, register_b, register_c)
            pc += 2
    return output.rstrip(",")


def produces_itself(instructions: list[int], register_a: int, register_b: int, register_c: int) -> bool:
    output = []

    pc = 0
    while pc < len(instructions):
        if instructions[pc] == 0:
            register_a = register_a // 2 ** get_combo_operand(instructions[pc + 1], register_a, register_b, register_c)
            pc += 2
        elif instructions[pc] == 1:
            register_b = register_b ^ instructions[pc + 1]
            pc += 2
        elif instructions[pc] == 2:
            register_b = get_combo_operand(instructions[pc + 1], register_a, register_b, register_c) % 8
            pc += 2
        elif instructions[pc] == 3:
            pc = instructions[pc + 1] if register_a != 0 else pc + 2
        elif instructions[pc] == 4:
            register_b = register_b ^ register_c
            pc += 2
        elif instructions[pc] == 5:
            output.append(get_combo_operand(instructions[pc + 1], register_a, register_b, register_c) % 8)
            if output[-1] != instructions[-1]:
                return False
            pc += 2
        elif instructions[pc] == 6:
            register_b = register_a // 2 ** get_combo_operand(instructions[pc + 1], register_a, register_b, register_c)
            pc += 2
        else:
            register_c = register_a // 2 ** get_combo_operand(instructions[pc + 1], register_a, register_b, register_c)
            pc += 2
    return len(instructions) == len(output)


# Task 2:
# Let's review the program:
# 0,3,5,4,3,0
# 1st command: 0,3
# 2nd command: 5,4
# 3rd command: 3,0


def main():
    from time import time
    print("=== 1 ===")
    print("Example result:", run_program(*parse_input("example-input.txt")))
    t = time()
    print("Task result:", run_program(*parse_input("input.txt")))
    print("Time for task:", (time() - t) * 1000, "ms")
    print("=== 2 ===")


if __name__ == '__main__':
    main()
