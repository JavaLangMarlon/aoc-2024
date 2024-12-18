from typing import Callable

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


def widen_board(board: list[list[int]]) -> tuple[list[list[int]], int, int]:
    new_board = []
    robot_i = -1
    robot_j = -1
    for row in board:
        new_board.append([])
        for cell in row:
            if cell == ROBOT:
                robot_i = len(new_board) - 1
                robot_j = len(new_board[-1])
                new_board[-1].append(ROBOT)
                new_board[-1].append(VOID)
            elif cell == BOX:
                new_board[-1].append(LEFT_BOX)
                new_board[-1].append(RIGHT_BOX)
            else:
                new_board[-1].append(cell)
                new_board[-1].append(cell)
    return new_board, robot_i, robot_j


def get_new_box_locations(board: list[list[int]], instruction: str,
                          i: int, js: set[int]) -> tuple[set[tuple[int, int]], set[tuple[int, int]], set[tuple[int, int]]] | None:
    new_voids = set()
    left_box_locations = set()
    right_box_locations = set()
    while len(js) != 0:
        new_js = set()
        new_i = i + 1 if instruction == "v" else i - 1

        for j in js:
            if board[i][j] == VOID:
                continue
            if board[i][j] == OBSTACLE:
                return None
            if board[i][j] == RIGHT_BOX:
                new_voids.add((i, j))
                new_voids.add((i, j - 1))
                left_box_locations.add((new_i, j - 1))
                right_box_locations.add((new_i, j))
                new_js.add(j - 1)
                new_js.add(j)
            else:
                new_voids.add((i, j))
                new_voids.add((i, j + 1))
                left_box_locations.add((new_i, j))
                right_box_locations.add((new_i, j + 1))
                new_js.add(j + 1)
                new_js.add(j)
        i = new_i
        js = new_js
    return new_voids, left_box_locations, right_box_locations



def calculate_gps_wide(board: list[list[int]], instructions: str, robot_i: int, robot_j: int) -> int:
    # we need to be aware of that scenario
    #      @
    #     []
    #     []
    #    [][]
    #   [][][]
    #  [][][][]
    # [][][][][]
    #          ##
    wide_board, robot_i, robot_j = widen_board(board)

    for instruction in instructions:
        if instruction == "^" or instruction == "v":
            move = directions[instruction]

            new_i, new_j = move(robot_i, robot_j)
            result = get_new_box_locations(wide_board, instruction, new_i, {new_j})
            if result is None:
                continue
            new_voids, left_box_locations, right_box_locations = result
            for i, j in new_voids:
                wide_board[i][j] = VOID
            for i, j in left_box_locations:
                wide_board[i][j] = LEFT_BOX
            for i, j in right_box_locations:
                wide_board[i][j] = RIGHT_BOX
            wide_board[robot_i][robot_j] = VOID
            wide_board[new_i][new_j] = ROBOT
            robot_i, robot_j = new_i, new_j
        else:
            move = directions[instruction]

            found_void = False
            new_i, new_j = move(robot_i, robot_j)
            while True:
                if wide_board[new_i][new_j] == OBSTACLE:
                    break
                if wide_board[new_i][new_j] == VOID:
                    found_void = True
                    break
                new_i, new_j = move(new_i, new_j)
            if not found_void:
                continue
            move_backward = directions[turn_around[instruction]]
            i, j = new_i, new_j
            while i != robot_i or j != robot_j:
                older_i, older_j = move_backward(i, j)
                wide_board[i][j] = wide_board[older_i][older_j]
                i, j = older_i, older_j
            wide_board[i][j] = VOID
            robot_i, robot_j = move(robot_i, robot_j)

    result = 0

    for i in range(len(wide_board)):
        for j in range(len(wide_board[i])):
            if wide_board[i][j] == BOX:
                result += 100 * i + j

    return result

def main():
    print("=== 1 ===")
    print("Example result:", calculate_gps(*parse_input("example-input.txt")))
    print("Task result:", calculate_gps(*parse_input("input.txt")))
    print("=== 2 ===")
    print("Example result:", calculate_gps_wide(*parse_input("example-input.txt")))
    print("Example result:", calculate_gps_wide(*parse_input("input.txt")))


if __name__ == '__main__':
    main()
