import re

import numpy as np
from scipy.optimize import milp, LinearConstraint


class ArcadeMachine:
    def __init__(self, a_x, a_y, b_x, b_y, a_coins, b_coins, price_x, price_y):
        self.a_x = a_x
        self.a_y = a_y
        self.b_x = b_x
        self.b_y = b_y
        self.a_coins = a_coins
        self.b_coins = b_coins
        self.price_x = price_x
        self.price_y = price_y

    def calculate_tokens_to_win(self, maximum_pressed: int | None) -> int | None:
        # we just perform bruteforce here
        i = 1
        minimum = float("inf")
        while i * self.a_x <= self.price_x and i * self.a_y <= self.price_y and \
                (maximum_pressed is None or i <= maximum_pressed):
            j = 0
            while True:
                if i * self.a_x + j * self.b_x > self.price_x or i * self.a_y + j * self.b_y > self.price_y or \
                        maximum_pressed is not None and j > maximum_pressed:
                    break
                if i * self.a_x + j * self.b_x == self.price_x and i * self.a_y + j * self.b_y == self.price_y:
                    if i * self.a_coins + j * self.b_coins < minimum:
                        minimum = i * self.a_coins + j * self.b_coins
                    break
                j += 1
            i += 1

        if minimum == float("inf"):
            return None
        return minimum

    def calculate_tokens_to_win_fast(self) -> int | None:
        # we use integer optimization here
        # we have a problem of the form
        # min_x c^T x
        #   s. t. b_l <= Ax <= b_u
        # in our particular case, we set the values to
        # c^T = [a_coins b_coins]
        # x = [i j]^T  (see above)
        # b_l = b_u = [price_x price_y]^T
        # A = [ a_x   b_x ]
        #     [ a_y   b_y ]
        c = np.array([self.a_coins, self.b_coins])
        b = np.array([self.price_x, self.price_y])
        A = np.array([[self.a_x, self.b_x], [self.a_y, self.b_y]])
        optim_result = milp(c, constraints=LinearConstraint(A, lb=b, ub=b))
        if optim_result.x is not None and (np.abs(optim_result.x - np.round(optim_result.x)) < 0.0001).all():
            return round(optim_result.fun)
        return None


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x, y = y1, x1 - (a // b) * y1
    return g, x, y


num_regex = re.compile(r"\d+")


def parse_input(path: str) -> list[ArcadeMachine]:
    result = []
    with open(path) as f:
        i = 0
        lines = f.read().split("\n")
        while i < len(lines):
            a = num_regex.findall(lines[i].strip())
            b = num_regex.findall(lines[i+1].strip())
            prize = num_regex.findall(lines[i+2].strip())

            result.append(ArcadeMachine(int(a[0]), int(a[1]), int(b[0]), int(b[1]), 3, 1, int(prize[0]), int(prize[1])))

            i += 4
    return result


def get_fewest_tokens(machines: list[ArcadeMachine], maximum_pushes: int | None, fast=False) -> int:
    result = 0
    for i in machines:
        if fast:
            tokens_to_win = i.calculate_tokens_to_win_fast()
        else:
            tokens_to_win = i.calculate_tokens_to_win(maximum_pushes)
        if tokens_to_win is not None:
            result += tokens_to_win
    return result


def increase_prize_location(input: list[ArcadeMachine]) -> list[ArcadeMachine]:
    for i in input:
        i.price_x += 10000000000000
        i.price_y += 10000000000000
    return input


def main():
    print("=== 1 ===")
    print("Example result:", get_fewest_tokens(parse_input("example-input.txt"), 100))
    print("Task result:", get_fewest_tokens(parse_input("input.txt"), 100))
    print("=== 2 ===")
    print("Example result:", get_fewest_tokens(increase_prize_location(parse_input("example-input.txt")), None, fast=True))
    print("Task result:", get_fewest_tokens(increase_prize_location(parse_input("input.txt")), None, fast=True))


if __name__ == "__main__":
    main()
