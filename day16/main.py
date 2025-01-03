from collections import defaultdict
from enum import Enum
import heapq

# This one is tough. My first idea was to view the maze as a graph and then run something like Dijkstra on it.
# The intersections of the maze and the start and end points would be nodes in that graph and the paths between these
# positions would be the links. A problem that would probably arise is that the weights of the links change
# depending on the reindeer's orientation because it costs to turn. One possible solution is to add a node for each
# orientation per intersection, so 4 nodes for 1 intersection.
#
# To create the graph, we go through the whole maze and for every path between two intersections, we add two links for
# each direction. If we see a new intersection, we also add the 3 other nodes.
# If the graph creation works correctly, applying Dijkstra and checking for the distance to a node with the end point
# and ignoring the direction gives us the right result.

class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3

class Node:
    def __init__(self, direction: Direction, i: int, j: int):
        """
        :param direction: direction the node is facing
        :param i: vertical coordinate in the maze matrix
        :param j: horizontal coordinate in the maze matrix
        """
        self.direction = direction
        self.i = i
        self.j = j

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.direction == other.direction and self.i == other.i \
            and self.j == other.j

    def __hash__(self):
        return hash((self.direction, self.i, self.j))

    def get_turned_around_version(self) -> 'Node':
        if self.direction == Direction.EAST:
            return Node(Direction.WEST, self.i, self.j)
        if self.direction == Direction.SOUTH:
            return Node(Direction.NORTH, self.i, self.j)
        if self.direction == Direction.WEST:
            return Node(Direction.EAST, self.i, self.j)
        return Node(Direction.SOUTH, self.i, self.j)


# the graph structure in this case is of the form dict[Node, list[list[Node | int]]]
# the keys here mark the source nodes of a link. The list then contains all connected target nodes with the weight
# of the corresponding link


def side_neighbors(i: int, j: int, facing_direction: Direction) -> tuple[Direction, int, int, Direction, int, int]:
    if facing_direction == Direction.EAST or facing_direction == Direction.WEST:
        return Direction.NORTH, i - 1, j, Direction.SOUTH, i + 1, j
    return Direction.WEST, i, j - 1, Direction.EAST, i, j + 1

def forward_neighbor(i: int, j: int, facing_direction: Direction) -> tuple[int, int]:
    if facing_direction == Direction.EAST:
        return i, j + 1
    if facing_direction == Direction.SOUTH:
        return i + 1, j
    if facing_direction == Direction.WEST:
        return i, j - 1
    return i - 1, j


def get_neighboring_node(maze: list[str], node: Node, step_penalty: int,
                          turn_penalty: int) -> tuple[Node, int, list[tuple[int, int]]] | None:
    """
    NOTE: an infinite loop will evolve here if the maze is an endless circle without intersections

    :return: intersection, so first position where there are two paths, or None the path leads into a dead end
    """
    distance = step_penalty
    i, j = forward_neighbor(node.i, node.j, node.direction)

    if maze[i][j] == "#":
        return None

    visited_cells = [(node.i, node.j), (i, j)]

    direction = node.direction
    while True:
        visited_cells.append((i, j))
        forward_i, forward_j = forward_neighbor(i, j, direction)
        side_direction_1, side_i_1, side_j_1, side_direction_2, side_i_2, side_j_2 = side_neighbors(i, j, direction)
        if i == len(maze) - 2 and j == 1 or i == 1 and j == len(maze[1]) - 2:
            return Node(direction, i, j), distance, visited_cells
        if maze[forward_i][forward_j] != "#":
            if maze[side_i_1][side_j_1] != "#" or maze[side_i_2][side_j_2] != "#":
                return Node(direction, i, j), distance, visited_cells
            distance += step_penalty
            i, j = forward_i, forward_j
        elif maze[side_i_1][side_j_1] != "#":
            if maze[side_i_2][side_j_2] != "#":
                return Node(direction, i, j), distance, visited_cells
            distance += step_penalty + turn_penalty
            direction, i, j = side_direction_1, side_i_1, side_j_1
        elif maze[side_i_2][side_j_2] != "#":
            distance += step_penalty + turn_penalty
            direction, i, j = side_direction_2, side_i_2, side_j_2
        else:
            return None


def add_nodes_for_intersection(graph: dict[Node, list[list[Node | int]]], i: int, j: int, turn_penalty: int) -> list:
    east_node = Node(Direction.EAST, i, j)
    south_node = Node(Direction.SOUTH, i, j)
    west_node = Node(Direction.WEST, i, j)
    north_node = Node(Direction.NORTH, i, j)

    # if we want to get the fastest path then turning around 180° will be pointless
    graph[east_node] = [
        [south_node, turn_penalty],
        [north_node, turn_penalty],
    ]
    graph[south_node] = [
        [west_node, turn_penalty],
        [east_node, turn_penalty],
    ]
    graph[west_node] = [
        [north_node, turn_penalty],
        [south_node, turn_penalty],
    ]
    graph[north_node] = [
        [west_node, turn_penalty],
        [east_node, turn_penalty],
    ]
    return [east_node, south_node, west_node, north_node]


def establish_link(graph: dict[Node, list[list[Node | int]]], source: Node, target: Node, distance: int):
    neighbor_index = -1
    for (index, neighbor) in enumerate(graph[source]):
        if neighbor == target:
            neighbor_index = index
            break
    if neighbor_index != -1:
        graph[source][neighbor_index][1] = min(distance, graph[target][neighbor_index][1])
    else:
        graph[source].append([target, distance])


def create_graph(maze: list[str], step_penalty=1,
                 turn_penalty=1000) -> tuple[dict[Node, list[list[Node, int]]], dict[tuple[Node, Node], list[tuple[int, int]]]]:
    """
    we assume here that the start position is in the bottom left and the end position is in the top right.
    """
    graph = {}
    nodes_to_go = []
    cells_of_links = {}

    start_nodes = add_nodes_for_intersection(graph, len(maze) - 2, 1, turn_penalty)
    nodes_to_go.extend(start_nodes)

    while len(nodes_to_go) != 0:
        current_node = nodes_to_go.pop(0)

        result = get_neighboring_node(maze, current_node, step_penalty, turn_penalty)
        if result is None:
            continue
        neighbor, distance, visited_cells = result
        if neighbor not in graph.keys():
            added_nodes = add_nodes_for_intersection(graph, neighbor.i, neighbor.j, turn_penalty)
            nodes_to_go.extend(added_nodes)
        establish_link(graph, current_node, neighbor, distance)
        cells_of_links[(current_node, neighbor)] = visited_cells
        cells_of_links[(neighbor, current_node)] = visited_cells

    return graph, cells_of_links


class DijkstraEntry:
    def __init__(self, node: Node, distances: dict[Node, int | float]):
        self.node = node
        self.distances = distances

    def __lt__(self, other: 'DijkstraEntry'):
        return self.distances[self.node] < self.distances[other.node]

def dijkstra(graph: dict[Node, list[list[Node, int]]], start_node: Node) -> tuple[dict[Node, int | float], dict[Node, list[Node]]]:
    resulting_distances = {}
    resulting_predecessors = defaultdict(list)
    distances = {node: float('inf') for node in graph.keys()}
    distances[start_node] = 0
    entries = [DijkstraEntry(start_node, distances)] + [DijkstraEntry(node, distances) for node in graph.keys()]
    heapq.heapify(entries)
    while len(entries) != 0:
        next_entry = heapq.heappop(entries)
        resulting_distances[next_entry.node] = distances[next_entry.node]
        changed = False
        for neighbor, distance_to_neighbor in graph[next_entry.node]:
            relaxed_distance = distances[next_entry.node] + distance_to_neighbor
            if relaxed_distance == distances[neighbor]:
                resulting_predecessors[neighbor].append(next_entry.node)
            if relaxed_distance < distances[neighbor]:
                resulting_predecessors[neighbor] = [next_entry.node]
                distances[neighbor] = relaxed_distance
                changed = True
        if changed:
            heapq.heapify(entries)
    return resulting_distances, resulting_predecessors


def collect_cells(cells_of_links: dict[tuple[Node, Node], list[tuple[int, int]]],
                  predecessors: dict[Node, list[Node]], nodes: list[Node]):
    cells = set()
    visited_nodes = set()
    while len(nodes) != 0:
        next_node = nodes.pop(0)
        visited_nodes.add(next_node)

        for predecessor in predecessors[next_node]:
            if (predecessor, next_node) in cells_of_links:
                for cell in cells_of_links[(predecessor, next_node)]:
                    cells.add(cell)
            if predecessor not in visited_nodes:
                nodes.append(predecessor)
    return cells


def shortest_distance(maze: list[str]) -> tuple[int, int]:
    graph, cells_of_links = create_graph(maze)

    shortest_distances, predecessors = dijkstra(graph, Node(Direction.EAST, len(maze) - 2, 1))

    min_distance = float('inf')
    min_nodes = []
    for i in [Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH]:
        node = Node(i, 1, len(maze[1]) - 2)
        if shortest_distances[node] < min_distance:
            min_distance = shortest_distances[node]
            min_nodes = [node]
        elif shortest_distances[node] == min_distance:
            min_nodes.append(node)

    return min_distance, len(collect_cells(cells_of_links, predecessors, min_nodes))

# This code can be easily extended to give a result for task 2. While we construct the graph, we also store all cells
# corresponding to a specific link when traversing the maze in get_neighboring_node. Then, when we do dijkstra, we also
# store the predecessors of each node (plural for the case that there are equally long paths). Eventually, we can count
# these paths

def parse_input(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def main():
    example_distance, example_cells_num = shortest_distance(parse_input("example-input.txt"))
    distance, cells_num = shortest_distance(parse_input("input.txt"))
    print("=== 1 ===")
    print("Example result:", example_distance)
    print("Task result:", distance)
    print("=== 2 ===")
    print("Example result:", example_cells_num)
    print("Task result:", cells_num)


if __name__ == '__main__':
    main()
