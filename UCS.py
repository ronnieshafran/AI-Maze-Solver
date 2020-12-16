from dataStructures import *
from Heuristics import zero_heuristic
from numpy import ndarray


def get_node_in_direction(parent_node: Node, direction: str, matrix: ndarray, h_function, end_point) -> Node:
    next_node_coordinates = None
    next_node_value = None
    try:
        if direction == "RU":
            next_node_coordinates = Point([parent_node.coordinates.x - 1, parent_node.coordinates.y + 1])
            next_node_value = matrix[parent_node.coordinates.x - 1][parent_node.coordinates.y + 1]
        elif direction == "R":
            next_node_coordinates = Point([parent_node.coordinates.x, parent_node.coordinates.y + 1])
            next_node_value = matrix[parent_node.coordinates.x][parent_node.coordinates.y + 1]
        elif direction == "RD":
            next_node_coordinates = Point([parent_node.coordinates.x + 1, parent_node.coordinates.y + 1])
            next_node_value = matrix[parent_node.coordinates.x + 1][parent_node.coordinates.y + 1]
        elif direction == "D":
            next_node_coordinates = Point([parent_node.coordinates.x + 1, parent_node.coordinates.y])
            next_node_value = matrix[parent_node.coordinates.x + 1][parent_node.coordinates.y]
        elif direction == "LD":
            next_node_coordinates = Point([parent_node.coordinates.x + 1, parent_node.coordinates.y - 1])
            next_node_value = matrix[parent_node.coordinates.x + 1][parent_node.coordinates.y - 1]
        elif direction == "L":
            next_node_coordinates = Point([parent_node.coordinates.x, parent_node.coordinates.y - 1])
            next_node_value = matrix[parent_node.coordinates.x][parent_node.coordinates.y - 1]
        elif direction == "LU":
            next_node_coordinates = Point([parent_node.coordinates.x - 1, parent_node.coordinates.y - 1])
            next_node_value = matrix[parent_node.coordinates.x - 1][parent_node.coordinates.y - 1]
        elif direction == "U":
            next_node_coordinates = Point([parent_node.coordinates.x - 1, parent_node.coordinates.y])
            next_node_value = matrix[parent_node.coordinates.x - 1][parent_node.coordinates.y]
        # verify it's not a wall or out of bounds
        if next_node_coordinates.x < 0 or next_node_coordinates.y < 0 or next_node_value < 0:
            return Node()
        next_node_h_value = h_function(next_node_coordinates, end_point)
        return Node(coordinates=next_node_coordinates, cost=next_node_value,path_to_node=parent_node.path_to_node + f'{direction}-',
                    depth= parent_node.depth +1,g_cost_of_path=parent_node.g_cost_of_path + next_node_value, heuristic_value=next_node_h_value)
            # next_node_coordinates, next_node_value, parent_node.path_to_node + f'{direction}-',
            #         parent_node.depth + 1, parent_node.f_cost_of_path + next_node_value + next_node_h_value, next_node_h_value
    except:
        return Node()


def get_children(node, matrix, h_function = zero_heuristic, end_point = Point([0,0])):
    children = []
    directions = ("RU", "R", "RD", "D", "LD", "L", "LU", "U")
    for direction in directions:
        current_node = get_node_in_direction(node, direction, matrix, h_function, end_point)
        if current_node.cost > 0:
            children.append(current_node)
    return children


# TODO: how to hint to a func type? failed googling it

def run(data: DataInput, h_function) -> AlgorithmResult:
    # init variables and add first node to queue
    queue = PriorityQueue()
    visited = {}
    min_depth = data.matrix_size ** 2
    max_depth = 0
    total_depth = 0
    start_node = Node(data.start_point, data.matrix[data.start_point.x][data.start_point.y])
    goal_node = Node()
    queue.insert(start_node, 0)

    while not queue.is_empty():
        current_node = queue.remove()
        if current_node.coordinates == data.end_point:
            goal_node = current_node
            break

        if current_node.depth > max_depth:
            max_depth = current_node.depth
        total_depth += current_node.depth

        visited |= {current_node.coordinates: current_node.f_cost_of_path}
        nodes_to_enqueue = get_children(current_node, data.matrix, h_function, data.end_point)

        # check for min depth when the search path is "stuck"
        if len(nodes_to_enqueue) == 0:
            min_depth = current_node.depth
        else:
            for node in nodes_to_enqueue:
                if node.coordinates not in visited:
                    queue.insert(node, node.f_cost_of_path)
                elif node.f_cost_of_path < visited.get(node.coordinates):
                    visited.pop(node.coordinates)
                    queue.insert(node, node.f_cost_of_path)

    total_expanded_nodes = len(visited)
    avg_depth = total_depth / total_expanded_nodes
    # TODO: how do you correctly calculate min depth in UCS?
    min_depth = max_depth if min_depth == data.matrix_size ** 2 else max_depth

    if goal_node.cost > 0:
        return AlgorithmResult(goal_node.path_to_node[:-1], goal_node.f_cost_of_path, total_expanded_nodes, 0,
                               True,
                               0, 0, min_depth, max_depth, avg_depth)
    else:
        return AlgorithmResult("", 0, total_expanded_nodes, 0, False, 0, 0, min_depth, max_depth, avg_depth)

    # repeat until queue is empty
