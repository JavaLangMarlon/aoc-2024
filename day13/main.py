import re

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


def get_fewest_tokens(machines: list[ArcadeMachine], maximum_pushes: int | None) -> int:
    result = 0
    for i in machines:
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
    print("Example result:", get_fewest_tokens(increase_prize_location(parse_input("example-input.txt")), None))
    # print("Task result:", get_fewest_tokens(increase_prize_location(parse_input("input.txt"))))


if __name__ == "__main__":
    main()
