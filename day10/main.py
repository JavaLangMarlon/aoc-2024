
def parse_input(path: str) -> list[list[int]]:
    board = []
    with open(path) as f:
        for line in f:
            board.append([int(c) for c in line.strip()])
    return board


def climb_up(board: list[list[int]], reached_tops: set, reached_positions: set, i: int, j: int):
    reached_positions.add((i, j))
    if board[i][j] == 9:
        reached_tops.add((i, j))
        return
    for (new_i, new_j) in [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]:
        if new_i < 0 or new_i >= len(board) or new_j < 0 or new_j >= len(board[0]) or \
                (new_i, new_j) in reached_positions or board[new_i][new_j] != board[i][j] + 1:
            continue
        climb_up(board, reached_tops, reached_positions, new_i, new_j)


def climb_up_with_rating(board: list[list[int]], i: int, j: int) -> int:
    if board[i][j] == 9:
        return 1
    result = 0
    for (new_i, new_j) in [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]:
        if new_i < 0 or new_i >= len(board) or new_j < 0 or new_j >= len(board[0]) or \
                board[new_i][new_j] != board[i][j] + 1:
            continue
        result += climb_up_with_rating(board, new_i, new_j)
    return result


def get_score(board: list[list[int]], rating=False) -> str:
    result = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                if rating:
                    result += climb_up_with_rating(board, i, j)
                else:
                    reached_tops = set()
                    reached_positions = set()
                    climb_up(board, reached_tops, reached_positions, i, j)
                    result += len(reached_tops)
    return result


def main():
    print("=== 1 ===")
    print("Example result:", get_score(parse_input("example-input.txt")))
    print("Task result:", get_score(parse_input("input.txt")))
    print("=== 2 ===")
    print("Example result:", get_score(parse_input("example-input.txt"), rating=True))
    print("Task result:", get_score(parse_input("input.txt"), rating=True))


if __name__ == "__main__":
    main()
