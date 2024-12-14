import re
import sys

import numpy as np
np.set_printoptions(threshold=sys.maxsize)

num_regex = re.compile(r'-?\d+')
digit_bar = re.compile(r'\d{4}\d+')

class Robot:
    def __init__(self, line: str):
        nums = num_regex.findall(line)
        self.x = int(nums[0])
        self.y = int(nums[1])
        self.v_x = int(nums[2])
        self.v_y = int(nums[3])


def parse_input(path: str) -> list[Robot]:
    result = []
    with open(path) as f:
        for line in f:
            result.append(Robot(line.strip()))
    return result


def calculate_safety(robots: list[num_regex], width: int, height: int, iterations: int) -> int:
    bathroom = np.zeros((height, width))
    for robot in robots:
        bathroom[(robot.y + iterations * robot.v_y) % height, (robot.x + iterations * robot.v_x) % width] += 1
    center_x, center_y = width // 2, height // 2
    return np.sum(bathroom[:center_y, :center_x]) * np.sum(bathroom[:center_y, center_x + 1:]) * \
           np.sum(bathroom[center_y + 1:, :center_x, ]) * np.sum(bathroom[center_y + 1:, center_x + 1:])


def print_christmas_tree(robots: list[num_regex], width: int, height: int, max_iterations: int):
    for i in range(1, max_iterations):
        bathroom = np.zeros((height, width))
        for robot in robots:
            bathroom[(robot.y + i * robot.v_y) % height, (robot.x + i * robot.v_x) % width] += 1
        lines = []
        should_print = False
        for row in bathroom:
            lines.append("".join([str(int(cell)) if int(cell) != 0 else "." for cell in list(row)]))
            if digit_bar.search(lines[-1]) is not None:
                should_print = True
        if should_print:
            print(f"{i}. iteration:")
            print("\n".join(lines))


def main():
    print("=== 1 ===")
    print("Example result:", calculate_safety(parse_input("example-input.txt"), 11, 7, 100))
    print("Task result:", calculate_safety(parse_input("input.txt"), 101, 103, 100))
    print("=== 2 ===")
    print("Task result:")
    print_christmas_tree(parse_input("input.txt"), 101, 103, 10000)
    # 7916.

if __name__ == '__main__':
    main()
