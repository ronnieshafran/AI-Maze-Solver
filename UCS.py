from dataStructures import *
from numpy import ndarray


def getNodeInDirection(parent_node: Node, direction: str, matrix: ndarray) -> Node:
    next_node_point = None
    next_node_value = None
    try:
        if direction == "RU":
            next_node_point = Point([parent_node.coordinates.x - 1, parent_node.coordinates.y + 1])
            next_node_value = matrix[parent_node.coordinates.x - 1][parent_node.coordinates.y + 1]
        elif direction == "R":
            next_node_point = Point([parent_node.coordinates.x, parent_node.coordinates.y + 1])
            next_node_value = matrix[parent_node.coordinates.x][parent_node.coordinates.y + 1]
        elif direction == "RD":
            next_node_point = Point([parent_node.coordinates.x + 1, parent_node.coordinates.y + 1])
            next_node_value = matrix[parent_node.coordinates.x + 1][parent_node.coordinates.y + 1]
        elif direction == "D":
            next_node_point = Point([parent_node.coordinates.x + 1, parent_node.coordinates.y])
            next_node_value = matrix[parent_node.coordinates.x + 1][parent_node.coordinates.y]
        elif direction == "LD":
            next_node_point = Point([parent_node.coordinates.x + 1, parent_node.coordinates.y - 1])
            next_node_value = matrix[parent_node.coordinates.x + 1][parent_node.coordinates.y - 1]
        elif direction == "L":
            next_node_point = Point([parent_node.coordinates.x, parent_node.coordinates.y - 1])
            next_node_value = matrix[parent_node.coordinates.x][parent_node.coordinates.y - 1]
        elif direction == "LU":
            next_node_point = Point([parent_node.coordinates.x - 1, parent_node.coordinates.y - 1])
            next_node_value = matrix[parent_node.coordinates.x - 1][parent_node.coordinates.y - 1]
        elif direction == "U":
            next_node_point = Point([parent_node.coordinates.x - 1, parent_node.coordinates.y])
            next_node_value = matrix[parent_node.coordinates.x - 1][parent_node.coordinates.y]

        if next_node_point.x < 0 or next_node_point.y < 0 or next_node_value < 0:
            return Node()
        return Node(next_node_point, next_node_value, parent_node.path_to_node + f'{direction}-',
                    parent_node.depth + 1, parent_node.cost_of_path + next_node_value)
    except:
        return Node()


def expandChildren(node, matrix):
    children = []
    directions = ("RU", "R", "RD", "D", "LD", "L", "LU", "U")
    for direction in directions:
        current_node = getNodeInDirection(node, direction, matrix)
        if current_node.cost > 0:
            children.append(current_node)
    return children


def run(data: DataInput) -> AlgorithmResult:
    queue = PriorityQueue()
    visited = set()
    min_depth = 0
    penertraion = 0  # TODO: what is this??
    EBF = 0  # TODO: what is this?
    avg_depth = 0  # TODO: where do we update this?
    start_node = Node(data.start_point, data.matrix[data.start_point.x][data.start_point.y])
    goal_node = Node()
    queue.insert(start_node, 0)
    visited.add(start_node.coordinates)

    while not queue.is_empty():
        current_node = queue.remove()
        if current_node.coordinates == data.end_point:
            goal_node = current_node
            break
        visited.add(current_node.coordinates)
        nodes_to_enqueue = expandChildren(current_node, data.matrix)
        if len(nodes_to_enqueue) == 0:
            min_depth = current_node.depth
        else:
            for node in nodes_to_enqueue:
                if (node.cost > 0) and (node.coordinates not in visited):
                    queue.insert(node, node.cost_of_path)

    total_expanded_nodes = len(visited)
    max_depth = goal_node.depth

    if goal_node.cost > 0:
        return AlgorithmResult(goal_node.path_to_node[:-1], goal_node.cost_of_path, total_expanded_nodes, penertraion,
                               True,
                               EBF, 0, min_depth, max_depth, avg_depth)
    else:
        return AlgorithmResult("", 0, total_expanded_nodes, 0, False, 0, 0, min_depth, max_depth, avg_depth)

    # repeat until queue is empty
