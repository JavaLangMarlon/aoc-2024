from sys import exit


step_directions = (
    lambda i, j: (i - 1, j),
    lambda i, j: (i, j + 1),
    lambda i, j: (i + 1, j),
    lambda i, j: (i, j - 1)
)

direction_letters = ("X", "Y", "Z", "A")  # letters were chosen arbitrarily


def parse_input(path: str) -> tuple[list[str], int, int]:
    i, j = -1, -1
    board = []
    with open(path) as f:
        for (line_index, line) in enumerate(f.readlines()):
            board.append(line.strip())
            if "^" in line:
                i = line_index
                j = line.index("^")
    if i == -1:
        print("error: position not found")
        exit(1)
    return board, i, j


def count_step(board: list[str], start_i, start_j) -> tuple[int, list[str]]:
    result = 0
    step_index = 0

    i = start_i
    j = start_j
    while True:
        if board[i][j] != "X":
            board[i] = board[i][:j] + "X" + board[i][j + 1:]
            result += 1

        for _ in range(4):
            new_i, new_j = step_directions[step_index](i, j)
            if not (0 <= new_i < len(board) and 0 <= new_j < len(board[0])):
                return result, board
            if board[new_i][new_j] != "#":
                i, j = new_i, new_j
                break
            step_index = (step_index + 1) % len(step_directions)
        else:
            print("error: got trapped")
            exit(1)

    # this code does not cover all scenarios that can lead to endless loops


def check_for_loop(board: list[list[list[str]]], start_i, start_j) -> bool:
    step_index = 0

    i = start_i
    j = start_j
    while True:
        if direction_letters[step_index] in board[i][j]:
            return True
        board[i][j].append(direction_letters[step_index])

        for _ in range(4):
            new_i, new_j = step_directions[step_index](i, j)
            if not (0 <= new_i < len(board) and 0 <= new_j < len(board[0])):
                return False
            if "#" not in board[new_i][new_j]:
                i, j = new_i, new_j
                break
            step_index = (step_index + 1) % len(step_directions)
        else:
            print("error: got trapped")
            exit(1)


# I am sorry, my work shift starts now and I could not come up with a better result
def count_loop_possibilities(board: list[str], start_i, start_j) -> int:
    # we modify the board to be able to store more information in one cell
    # as we want to know all directions that the cell has been visited with
    result = 0

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ".":
                mod_board = [[[cell] for cell in row] for row in board]
                mod_board[i][j] = ["#"]
                if check_for_loop(mod_board, start_i, start_j):
                    result += 1
    return result


def main():
    print("=== 1 ===")
    steps, board = count_step(*parse_input("example-input.txt"))
    print("Example result: {}\nBoard steps:\n{}".format(steps, "\n".join(board)))
    print(f"Task result: {count_step(*parse_input('input.txt'))[0]}")
    print("=== 2 ===")
    print("Example result:", count_loop_possibilities(*parse_input("example-input.txt")))
    # this function takes AGES to run HAHAHAHA (but produces the correct result so idc =) )
    print("Task result:", count_loop_possibilities(*parse_input("input.txt")))

if __name__ == '__main__':
    main()
