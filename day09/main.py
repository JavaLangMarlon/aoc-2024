
def parse_input(path: str) -> str:
    with open(path) as file:
        return file.read().strip()


def checksum_of_refactored_filesystem(filesystem: str) -> int:
    inflated_fs = []
    for (index, char) in enumerate(filesystem):
        if index % 2 == 0:
            inflated_fs += [str(int(index/2))] * int(char)
        else:
            inflated_fs += ["."] * int(char)
    ascending_i = 0
    for descending_i in range(len(inflated_fs) - 1, -1, -1):
        if inflated_fs[descending_i] == ".":
            continue
        while ascending_i < descending_i:
            if inflated_fs[ascending_i] != ".":
                ascending_i += 1
                continue
            inflated_fs[ascending_i] = inflated_fs[descending_i]
            inflated_fs[descending_i] = "."
            ascending_i += 1
            break
        else:
            break
    checksum = 0
    for (index, char) in enumerate(inflated_fs):
        if char != ".":
            checksum += int(char) * index
    return checksum


def update_free_spaces(free_spaces: list[list[int]], start, block_size):
    for i in range(len(free_spaces)):
        if free_spaces[i][0] + free_spaces[i][1] == start:
            free_spaces[i][1] += block_size
            if i + 1 < len(free_spaces) and free_spaces[i + 1][0] == start + block_size:
                free_spaces[i][1] += free_spaces[i + 1][1]
                del free_spaces[i + 1]
            break
        elif free_spaces[i][0] > start:
            free_spaces.insert(i, [start, block_size])
            break


def checksum_of_unfragmented_refactored_filesystem(filesystem: str) -> int:
    inflated_fs = []
    free_spaces = []
    for (index, char) in enumerate(filesystem):
        if index % 2 == 0:
            inflated_fs += [int(index / 2)] * int(char)
        else:
            free_spaces.append([len(inflated_fs), int(char)])
            inflated_fs += ["."] * int(char)

    visited_nums = set()
    descending_i = len(inflated_fs) - 1
    while descending_i >= 0:
        if inflated_fs[descending_i] == ".":
            descending_i -= 1
            continue
        current_num = inflated_fs[descending_i]
        if current_num in visited_nums:
            descending_i -= 1
            continue
        visited_nums.add(current_num)
        start = descending_i
        while start - 1 > -1 and inflated_fs[start - 1] == current_num:
            start -= 1
        block_width = descending_i - start + 1
        for spaces_index in range(len(free_spaces)):
            if free_spaces[spaces_index][1] >= block_width and free_spaces[spaces_index][0] < start:
                inflated_fs[free_spaces[spaces_index][0] : free_spaces[spaces_index][0] + block_width] = (
                        [current_num] * block_width)
                inflated_fs[start:descending_i + 1] = ["."] * block_width

                free_spaces[spaces_index] = [free_spaces[spaces_index][0] + block_width,
                                             free_spaces[spaces_index][1] - block_width]
                update_free_spaces(free_spaces, start, block_width)

                break
        descending_i = start - 1

    checksum = 0
    for (index, char) in enumerate(inflated_fs):
        if char != ".":
            checksum += int(char) * index
    return checksum


def main():
    print("=== 1 ===")
    print("Example input:", checksum_of_refactored_filesystem(parse_input("example-input.txt")))
    print("Task input:", checksum_of_refactored_filesystem(parse_input("input.txt")))
    print("=== 2 ===")
    print("Example input:", checksum_of_unfragmented_refactored_filesystem(parse_input("example-input.txt")))
    print("Task input:", checksum_of_unfragmented_refactored_filesystem(parse_input("input.txt")))


if __name__ == '__main__':
    main()
