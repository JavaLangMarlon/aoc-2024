from collections import defaultdict
from math import log10


def parse_input(path: str) -> list[int]:
    with open(path) as f:
        return [int(i) for i in f.read().split() if len(i.strip()) != 0]


def count_stones(stones: list[int], blinks=25) -> int:
    # further improvement could be reached by caching the calculation results over multiple blinks
    stones_dict = defaultdict(int)
    for stone in stones:
        stones_dict[stone] += 1
    for blink in range(blinks):
        additions = []
        removals = []
        for key in stones_dict.keys():
            val = stones_dict[key]
            if val == 0:
                continue
            if key == 0:
                removals.append((0, val))
                additions.append((1, val))
            elif int(log10(key)) % 2 == 1:
                str_rep = str(key)
                removals.append((key, val))
                additions.append((int(str_rep[:len(str_rep)//2]), val))
                additions.append((int(str_rep[len(str_rep)//2:]), val))
            else:
                removals.append((key, val))
                additions.append((key * 2024, val))
        for key, val in additions:
            stones_dict[key] += val
        for key, val in removals:
            stones_dict[key] -= val
    result = 0
    for val in stones_dict.values():
        result += val
    return result


def count_stones_old(stones: list[int], blinks=25) -> int:
    for blink in range(blinks):
        print(f"{blink+1}/{blinks}")
        stone_i = 0
        while stone_i < len(stones):
            if stones[stone_i] == 0:
                stones[stone_i] = 1
                stone_i += 1
            elif int(log10(stones[stone_i])) % 2 == 1:
                str_rep = str(stones[stone_i])
                stones[stone_i] = int(str_rep[:len(str_rep)//2])
                stones.insert(stone_i + 1, int(str_rep[len(str_rep)//2:]))
                stone_i += 2
            else:
                stones[stone_i] *= 2024
                stone_i += 1
    return len(stones)


def main():
    print("=== 1 ===")
    print("Example result:", count_stones(parse_input("example-input.txt"), blinks=6))
    print("Task result:", count_stones(parse_input("input.txt")))
    print("=== 2 ===")
    print("Task result:", count_stones(parse_input("input.txt"), blinks=75))


if __name__ == '__main__':
    main()
