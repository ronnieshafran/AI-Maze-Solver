from commonFunctions import *
from sys import maxsize


def run(data: DataInput, h_function) -> AlgorithmResult:
    start_time = time.process_time()
    # init variables
    open_list_queue = PriorityQueue()
    visited = {}
    min_depth = maxsize
    max_depth = 0
    total_expanded_nodes = 0
    total_depth = 0
    total_attempts = 0
    total_h = 0
    start_node = Node(data.start_point, data.matrix[data.start_point.x][data.start_point.y])
    goal_node = None
    open_list_queue.insert(start_node, 0)

    while not open_list_queue.is_empty():
        current_node = open_list_queue.remove()
        if current_node.coordinates in visited:
            continue
        total_expanded_nodes += 1
        total_h += current_node.heuristic_value

        # goal reached
        if current_node.coordinates == data.end_point:
            max_depth, min_depth, total_attempts, total_depth = calculate_depth_stats_on_cutoff(current_node, max_depth, min_depth,
                                                                                                total_attempts, total_depth)
            goal_node = current_node
            break

        visited |= {current_node.coordinates: current_node.f_cost_of_path}
        nodes_to_enqueue = [child for child in get_children(current_node, data.matrix, h_function, data.end_point) if
                            child.coordinates not in current_node.list_of_cords]
        nodes_enqueued = 0
        # cutoff
        if len(nodes_to_enqueue) == 0:
            max_depth, min_depth, total_attempts, total_depth = calculate_depth_stats_on_cutoff(current_node, max_depth, min_depth,
                                                                                                total_attempts, total_depth)
        else:
            for node in nodes_to_enqueue:
                if node.coordinates not in visited:
                    nodes_enqueued += 1
                    open_list_queue.insert(node, node.f_cost_of_path)

                elif node.f_cost_of_path < visited.get(node.coordinates):
                    nodes_enqueued += 1
                    visited.pop(node.coordinates)
                    open_list_queue.insert(node, node.f_cost_of_path)
        if nodes_enqueued == 0:
            max_depth, min_depth, total_attempts, total_depth = calculate_depth_stats_on_cutoff(current_node, max_depth, min_depth,
                                                                                                total_attempts, total_depth)

    # calculation of final stats
    avg_depth = round(total_depth / total_attempts, 2)
    avg_h = round(total_h / total_expanded_nodes, 2)
    # determine final depth for EBF / d/N stats
    if goal_node is not None:
        final_depth = goal_node.depth
    else:
        final_depth = max_depth
    EBF = round(total_expanded_nodes ** (1 / final_depth), 2)
    penetration = round(final_depth / total_expanded_nodes, 2)
    min_depth = max_depth if min_depth == maxsize else min_depth
    end_time = time.process_time()
    runtime = round(end_time - start_time, 4)
    if goal_node is not None:
        return AlgorithmResult(goal_node.path_to_node[:-1], goal_node.g_cost_of_path, total_expanded_nodes, penetration,
                               True,
                               EBF, avg_h, min_depth, max_depth, avg_depth, runtime)
    else:

        return AlgorithmResult("", 0, total_expanded_nodes, penetration, False, EBF, avg_h, min_depth, max_depth, avg_depth, runtime)


def calculate_depth_stats_on_cutoff(current_node, max_depth, min_depth, total_attempts, total_depth):
    if current_node.depth > max_depth:
        max_depth = current_node.depth
    if current_node.depth < min_depth:
        min_depth = current_node.depth
    total_depth += current_node.depth
    total_attempts += 1
    return max_depth, min_depth, total_attempts, total_depth
