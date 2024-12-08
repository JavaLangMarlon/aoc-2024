import itertools

def parse_input(path: str) -> list[str]:
    board = []
    with open(path) as f:
        for line in f:
            board.append(line.strip())
    return board


def calculate_unique_locations(board: list[str], with_harmony=False) -> int:
    locations_of_letters: dict[str, list[tuple[int, int]]] = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != '.':
                if board[i][j] in locations_of_letters:
                    locations_of_letters[board[i][j]].append((i, j))
                else:
                    locations_of_letters[board[i][j]] = [(i, j)]
    antinode_locations = set()
    for letter_locations in locations_of_letters.values():
        for ((i1, j1), (i2, j2)) in itertools.product(letter_locations, repeat=2):
            if i1 == i2 and j1 == j2:
                continue
            if with_harmony:
                k = 0
                antinode = (i2 + k * (i2 - i1), j2 + k * (j2 - j1))
                while 0 <= antinode[0] < len(board) and 0 <= antinode[1] < len(board[0]):
                    antinode_locations.add(antinode)
                    k += 1
                    antinode = (i2 + k * (i2 - i1), j2 + k * (j2 - j1))
            else:
                antinode = (i2 + i2 - i1, j2 + j2 - j1)
                if 0 <= antinode[0] < len(board) and 0 <= antinode[1] < len(board[0]):
                    antinode_locations.add(antinode)
    return len(antinode_locations)


def main():
    print("=== 1 ===")
    print("Example input:", calculate_unique_locations(parse_input("example-input.txt")))
    print("Task input:", calculate_unique_locations(parse_input("input.txt")))
    print("=== 2 ===")
    print("Example input:", calculate_unique_locations(parse_input("example-input.txt"), True))
    print("Task input:", calculate_unique_locations(parse_input("input.txt"), True))


if __name__ == '__main__':
    main()
