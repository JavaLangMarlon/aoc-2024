def parse_input(path: str) -> list[list[int, int]]:
    with open(path) as f:
        return [[int(num) for num in line.split(",")] for line in f.readlines()]


def construct_board(obstacles: list[list[int, int]], width: int, height: int, amount: int) -> list[list[bool]]:
    board = []
    for i in range(height):
        board.append([True] * width)
    added_obstacles = 0
    for obstacle_x, obstacle_y in obstacles:
        if added_obstacles == amount:
            break
        board[obstacle_y][obstacle_x] = False
        added_obstacles += 1
    return board


def neighbors(board: list[list[bool]], i: int, j: int) -> list[tuple[int, int]]:
    result = []
    for pot_i, pot_j in [
        (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)
    ]:
        if 0 <= pot_i < len(board) and 0 <= pot_j < len(board[0]) and board[pot_i][pot_j]:
            result.append((pot_i, pot_j))
    return result


def breadth_first_search(board: list[list[bool]], start_i: int, start_j: int,
                         end_i: int, end_j: int) -> int | None:
    """
    :return: amount of steps to reach the goal and the visited positions for task 2 or None if no path exists
    """
    steps = 0
    current_nodes = [(start_i, start_j)]
    visited_positions = set(current_nodes)
    while (end_i, end_j) not in visited_positions:
        steps += 1
        new_current_nodes = set()
        for node_i, node_j in current_nodes:
            for neighbor_i, neighbor_j in neighbors(board, node_i, node_j):
                if (neighbor_i, neighbor_j) not in visited_positions:
                    new_current_nodes.add((neighbor_i, neighbor_j))
        if len(new_current_nodes) == 0:
            return None
        current_nodes = new_current_nodes
        for curr in current_nodes:
            visited_positions.add(curr)
    return steps


def print_board(board):
    for i in board:
        print("".join(["." if j else "#" for j in i]))


def calculate_shortest_path(obstacles: list[list[int, int]], width: int, height: int, amount: int) -> int:
    board = construct_board(obstacles, width, height, amount)
    return breadth_first_search(board, 0, 0, width - 1, height - 1)


def calculate_first_blocking_obstacle(obstacles: list[list[int, int]], width: int, height: int, amount: int) -> tuple[int, int]:
    board = construct_board(obstacles, width, height, amount)
    # let's see if bruteforcing works here :)
    for obs_x, obs_y in obstacles[amount:]:
        board[obs_y][obs_x] = False
        if breadth_first_search(board, 0, 0, width - 1, height - 1) is None:
            return obs_x, obs_y
    return -1, -1  # None is blocking (should not occur in this context)


def main():
    print("=== 1 ===")
    print("Example result: ", calculate_shortest_path(parse_input("example-input.txt"), 7, 7, 12))
    print("Task result: ", calculate_shortest_path(parse_input("input.txt"), 71, 71, 1024))
    print("=== 2 ===")
    print("Example result: ", calculate_first_blocking_obstacle(parse_input("example-input.txt"), 7, 7, 12))
    print("Task result: ", calculate_first_blocking_obstacle(parse_input("input.txt"), 71, 71, 1024))


if __name__ == "__main__":
    main()
