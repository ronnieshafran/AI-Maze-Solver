from dataStructures import *
from commonFunctions import *
from Heuristics import zero_heuristic
from numpy import ndarray
import time


# TODO: how to hint to a func type? failed googling it

def run(data: DataInput, h_function) -> AlgorithmResult:
    start_time = time.process_time()
    # init variables and add first node to queue
    open_list_queue = PriorityQueue()
    visited = {}
    min_depth = data.matrix_size ** 2
    max_depth = 0
    total_depth = 0
    total_h = 0
    start_node = Node(data.start_point, data.matrix[data.start_point.x][data.start_point.y])
    goal_node = Node()
    open_list_queue.insert(start_node, 0)

    while not open_list_queue.is_empty():
        current_node = open_list_queue.remove()
        if current_node.coordinates in visited and current_node.f_cost_of_path >= visited.get(current_node.coordinates):
            continue

        # statistics calculation
        if current_node.depth > max_depth:
            max_depth = current_node.depth
        total_depth += current_node.depth
        total_h += current_node.heuristic_value

        if current_node.coordinates == data.end_point:
            goal_node = current_node
            break

        visited |= {current_node.coordinates: current_node.f_cost_of_path}
        nodes_to_enqueue = get_children(current_node, data.matrix, h_function, data.end_point)

        # check for min depth when the search path is "stuck"
        if len(nodes_to_enqueue) == 0:
            min_depth = current_node.depth
        else:
            for node in nodes_to_enqueue:
                if node.coordinates not in visited:
                    open_list_queue.insert(node, node.f_cost_of_path)

                elif node.f_cost_of_path < visited.get(node.coordinates):
                    visited.pop(node.coordinates)
                    open_list_queue.insert(node, node.f_cost_of_path)

    total_expanded_nodes = len(visited)
    avg_depth = round(total_depth / total_expanded_nodes, 2)
    avg_h = round(total_h / total_expanded_nodes, 2)
    EBF = round(total_expanded_nodes ** (1 / max_depth), 2)
    penetration = round(max_depth / total_expanded_nodes, 2)
    min_depth = max_depth if min_depth == data.matrix_size ** 2 else max_depth
    end_time = time.process_time()
    runtime = round(end_time - start_time, 4)
    if goal_node.cost > 0:
        return AlgorithmResult(goal_node.path_to_node[:-1], goal_node.g_cost_of_path, total_expanded_nodes, penetration,
                               True,
                               EBF, avg_h, min_depth, max_depth, avg_depth, runtime)
    else:

        return AlgorithmResult("", 0, total_expanded_nodes, penetration, False, EBF, avg_h, min_depth, max_depth, avg_depth, runtime)

    # repeat until queue is empty
