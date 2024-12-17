
VOID = 0
OBSTACLE = 1
BOX = 2
LEFT_BOX = 2
RIGHT_BOX = 3
ROBOT = 4

directions = {
    ">": lambda i, j: (i, j + 1),
    "<": lambda i, j: (i, j - 1),
    "^": lambda i, j: (i - 1, j),
    "v": lambda i, j: (i + 1, j),
}

turn_around = {
    ">": "<",
    "<": ">",
    "^": "v",
    "v": "^"
}

def parse_input(path: str) -> tuple[list[list[int]], str, int, int]:
    board = []
    instructions = ""
    i, j = -1, -1
    with open(path) as f:
        saw_delimiter = False
        for line in f:
            stripped_line = line.strip()
            if stripped_line == "":
                saw_delimiter = True
            if saw_delimiter:
                instructions += stripped_line
            else:
                board.append([])
                for char in stripped_line:
                    if char == ".":
                        board[-1].append(VOID)
                    elif char == "#":
                        board[-1].append(OBSTACLE)
                    elif char == "O":
                        board[-1].append(BOX)
                    elif char == "@":
                        if i > -1 or j > -1:
                            raise Exception()
                        i = len(board) - 1
                        j = len(board[-1])
                        board[-1].append(ROBOT)
    if i == -1 or j == -1:
        raise Exception()
    return board, instructions, i, j


# TODO remove
def print_board(board: list[list[int]]):
    chars = [".", "#", "O", "@"]
    for i in board:
        for j in i:
            print(chars[j], end="")
        print()
    print("?????????????????????????????????????????????????")


def calculate_gps(board: list[list[int]], instructions: str, robot_i: int, robot_j: int) -> int:
    for instruction in instructions:
        move = directions[instruction]

        found_void = False
        new_i, new_j = move(robot_i, robot_j)
        while True:
            if board[new_i][new_j] == OBSTACLE:
                break
            if board[new_i][new_j] == VOID:
                found_void = True
                break
            new_i, new_j = move(new_i, new_j)
        if not found_void:
            continue
        move_backward = directions[turn_around[instruction]]
        i, j = new_i, new_j
        while i != robot_i or j != robot_j:
            older_i, older_j = move_backward(i, j)
            board[i][j] = board[older_i][older_j]
            i, j = older_i, older_j
        board[i][j] = VOID
        robot_i, robot_j = move(robot_i, robot_j)

    result = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == BOX:
                result += 100 * i + j

    return result


def widen_board(board: list[list[int]]) -> list[list[int]]:
    new_board = []
    for row in board:
        new_board.append([])
        for cell in row:
            if cell == ROBOT:
                new_board[-1].append(ROBOT)
                new_board[-1].append(VOID)
            else:
                new_board[-1].append(cell)
                new_board[-1].append(cell)
    return new_board


def calculate_gps_wide(board: list[list[int]], instructions: str, robot_i: int, robot_j: int) -> int:
    wide_board = widen_board(board)


def main():
    print("=== 1 ===")
    print("Example result:", calculate_gps(*parse_input("example-input.txt")))
    print("Task result:", calculate_gps(*parse_input("input.txt")))
    print("=== 2 ===")
    print("Example result:", calculate_gps_wide(*parse_input("example-input.txt")))
    print("Example result:", calculate_gps_wide(*parse_input("example-input.txt")))


if __name__ == '__main__':
    main()
