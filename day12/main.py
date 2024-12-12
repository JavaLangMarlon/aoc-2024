from collections.abc import Callable


def parse_input(path: str) -> list[str]:
    with open(path) as f:
        # assuming that all rows have the same length
        return f.read().split("\n")


def walk_region(board: list[str], i: int, j: int, visited_locations: set) -> tuple[int, int]:
    area, perimeter = 1, 0
    visited_locations.add((i,j))
    for (new_i, new_j) in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if (new_i, new_j) in visited_locations:
            if board[new_i][new_j] != board[i][j]:
                perimeter += 1
        elif 0 <= new_i < len(board) and 0 <= new_j < len(board[0]) and board[new_i][new_j] == board[i][j]:
            more_area, more_perimeter = walk_region(board, new_i, new_j, visited_locations)
            area += more_area
            perimeter += more_perimeter
        else:
            perimeter += 1
    return area, perimeter


def is_side_already_occupied(board: list[str], i: int, j: int,
                             fence_and_neighbors: tuple[set, Callable[[int, int], tuple[int, int]], Callable[[int, int], tuple[int, int]]],
                             side_function: Callable[[int, int], tuple[int, int]]) -> bool:
    side_already_occupied = False
    neighbor_i, neighbor_j = fence_and_neighbors[1](i, j)
    while 0 <= neighbor_i < len(board) and 0 <= neighbor_j < len(board[0]) and \
            board[neighbor_i][neighbor_j] == board[i][j]:
        side_i, side_j = side_function(neighbor_i, neighbor_j)
        if 0 <= side_i < len(board) and 0 <= side_j < len(board[0]) and board[side_i][side_j] == board[i][j]:
            break
        if (neighbor_i, neighbor_j) in fence_and_neighbors[0]:
            side_already_occupied = True
            break
        neighbor_i, neighbor_j = fence_and_neighbors[1](neighbor_i, neighbor_j)
    if not side_already_occupied:
        neighbor_i, neighbor_j = fence_and_neighbors[2](i, j)
        while 0 <= neighbor_i < len(board) and 0 <= neighbor_j < len(board[0]) and board[neighbor_i][neighbor_j] == board[i][j]:
            side_i, side_j = side_function(neighbor_i, neighbor_j)
            if 0 <= side_i < len(board) and 0 <= side_j < len(board[0]) and board[side_i][side_j] == board[i][j]:
                break
            if (neighbor_i, neighbor_j) in fence_and_neighbors[0]:
                side_already_occupied = True
                break
            neighbor_i, neighbor_j = fence_and_neighbors[2](neighbor_i, neighbor_j)
    return side_already_occupied


def walk_region_with_bulk(board: list[str], i: int, j: int, visited_locations: set,
                          left_fence: set, right_fence: set, upper_fence: set, lower_fence: set) -> tuple[int, int]:
    area, perimeter = 1, 0
    visited_locations.add((i, j))
    fences_and_neighbors = (
        (lower_fence, lambda i, j: (i, j - 1), lambda i, j: (i, j + 1)),
        (upper_fence, lambda i, j: (i, j - 1), lambda i, j: (i, j + 1)),
        (right_fence, lambda i, j: (i - 1, j), lambda i, j: (i + 1, j)),
        (left_fence, lambda i, j: (i - 1, j), lambda i, j: (i + 1, j)),
    )
    side_functions = (
        lambda i, j: (i + 1, j),
        lambda i, j: (i - 1, j),
        lambda i, j: (i, j + 1),
        lambda i, j: (i, j - 1)
    )

    for (index, side_function) in enumerate(side_functions):
        new_i, new_j = side_function(i, j)
        if (new_i, new_j) in visited_locations:
            if board[new_i][new_j] != board[i][j]:
                if not is_side_already_occupied(board, i, j, fences_and_neighbors[index], side_function):
                    perimeter += 1
                fences_and_neighbors[index][0].add((i, j))
        elif 0 <= new_i < len(board) and 0 <= new_j < len(board[0]) and board[new_i][new_j] == board[i][j]:
            more_area, more_perimeter = walk_region_with_bulk(board, new_i, new_j, visited_locations,
                                                              left_fence, right_fence, upper_fence, lower_fence)
            area += more_area
            perimeter += more_perimeter
        else:
            if not is_side_already_occupied(board, i, j, fences_and_neighbors[index], side_function):
                perimeter += 1
            fences_and_neighbors[index][0].add((i, j))
    return area, perimeter


def calculate_fence_price(board: list[str], bulk=False) -> int:
    visited_locations = set()
    price = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if (i, j) not in visited_locations:
                if bulk:
                    area, perimeter = walk_region_with_bulk(board, i, j, visited_locations, set(), set(), set(), set())
                else:
                    area, perimeter = walk_region(board, i, j, visited_locations)
                price += area * perimeter
    return price


def main():
    print("=== 1 ===")
    print("Example result:", calculate_fence_price(parse_input("example-input.txt")))
    print("Task result:", calculate_fence_price(parse_input("input.txt")))
    print("=== 2 ===")
    print("Example result:", calculate_fence_price(parse_input("example-input.txt"), bulk=True))
    print("Task result:", calculate_fence_price(parse_input("input.txt"), bulk=True))


if __name__ == '__main__':
    main()
