from dataStructures import *
from queue import LifoQueue
from UCS import get_children


def DLS(matrix, matrix_size, start_point, end_point, search_depth) -> (AlgorithmResult, bool):
    # DLS without duplicates - every node enters the stack at most once
    stack = LifoQueue()
    observed_points_set = set()  # meant to avoid observing the same node twice if two nodes led to it
    total_expanded_nodes = 0
    min_depth = matrix_size - 1
    max_depth = 0
    total_depth = 0
    start_node = Node(start_point, matrix[start_point.x][start_point.y])
    goal_node = None
    remaining_nodes = False

    stack.put(start_node)
    observed_points_set.add(start_node.coordinates)
    while not stack.empty():
        current_node = stack.get()
        if current_node.depth > search_depth:
            remaining_nodes = True
            break

        total_expanded_nodes += 1
        total_depth += current_node.depth
        max_depth = current_node.depth if current_node.depth > max_depth else max_depth

        if current_node.coordinates == end_point:
            goal_node = current_node
            break

        children_nodes = get_children(current_node, matrix)
        children_nodes_to_put_in_stack = [child_node for child_node in children_nodes
                                          if child_node.coordinates not in observed_points_set]
        children_nodes_to_put_in_stack.reverse()

        if len(children_nodes_to_put_in_stack) == 0:
            min_depth = current_node.depth if current_node.depth < min_depth else min_depth
        else:
            for child_node in children_nodes_to_put_in_stack:
                stack.put(child_node)
                observed_points_set.add(child_node.coordinates)

    avg_depth = total_depth / total_expanded_nodes
    if goal_node is not None:
        return (AlgorithmResult(goal_node.path_to_node[:-1], goal_node.g_cost_of_path, total_expanded_nodes, 0, True, 0, 0,
                                min_depth, max_depth, avg_depth), remaining_nodes)
    else:
        return (AlgorithmResult("", 0, total_expanded_nodes, 0, False, 0, 0, min_depth, max_depth, avg_depth), remaining_nodes)


def run(data: DataInput) -> AlgorithmResult:
    current_search = None
    depth = 0
    remaining_nodes = True
    successful = False
    while remaining_nodes and not successful:
        current_search = DLS(data.matrix, data.matrix_size, data.start_point, data.end_point, depth)
        successful = current_search[0].successful
        remaining_nodes = current_search[1]
        depth += 1
    return current_search[0]
