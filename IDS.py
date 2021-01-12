import time

from dataStructures import *
from queue import LifoQueue
from UCS import get_children
from math import log2
from sys import maxsize


def DLS(matrix, matrix_size, start_point, end_point, search_depth, min_value) -> (AlgorithmResult, bool):
    stack = LifoQueue()
    observed_points_set = set()  # meant to avoid observing the same node twice if two nodes led to it
    total_expanded_nodes = 0
    min_depth = matrix_size - 1
    max_depth = 0
    total_depth = 0
    total_attempts = 0
    start_node = Node(start_point, matrix[start_point.x][start_point.y])
    goal_node = None
    remaining_nodes = False

    stack.put(start_node)
    observed_points_set.add(start_node.coordinates)
    while not stack.empty():

        current_node = stack.get()

        max_depth = current_node.depth if current_node.depth > max_depth else max_depth

        if current_node.coordinates == end_point:
            min_depth, total_depth = update_stats_at_cutoff(current_node, min_depth, total_attempts, total_depth)
            goal_node = current_node
            break

        if current_node.depth >= search_depth:
            min_depth, total_depth = update_stats_at_cutoff(current_node, min_depth, total_attempts, total_depth)
            remaining_nodes = True
            continue

        total_expanded_nodes += 1
        observed_points_set.add(current_node.coordinates)
        children_nodes = get_children(current_node, matrix, min_value=min_value)
        children_nodes.reverse()  # reverse order to maintain correct expansion pattern
        if len(children_nodes) == 0:
            min_depth, total_depth = update_stats_at_cutoff(current_node, min_depth, total_attempts, total_depth)

        for node in children_nodes:
            if node.coordinates in observed_points_set:
                continue
            else:
                stack.put(node)

    if goal_node is not None:
        return (AlgorithmResult(goal_node.path_to_node[:-1], goal_node.g_cost_of_path, total_expanded_nodes, 0, True, 0, 0,
                                min_depth, max_depth, total_depth), remaining_nodes)
    else:
        return AlgorithmResult("", 0, total_expanded_nodes, 0, False, 0, 0, min_depth, max_depth, total_depth), remaining_nodes


def update_stats_at_cutoff(current_node, min_depth, total_attempts, total_depth):
    total_depth += current_node.depth
    total_attempts += 1
    min_depth = current_node.depth if current_node.depth < min_depth else min_depth
    return min_depth, total_depth


def run(data: DataInput, start_time, total_runtime) -> AlgorithmResult:
    total_runtime = total_runtime if total_runtime > 0 else round(log2(data.matrix_size), 2)
    current_search = None
    depth = 0
    remaining_nodes = True
    successful = False
    total_nodes_expanded = 0
    total_depth = 0
    min_depth = maxsize
    while remaining_nodes and not successful:
        current_time = time.process_time()
        if current_time - start_time >= total_runtime:
            print("Out of time!")
            break
        # current_search returns tuple: (AlgorithmResult result, boolean remaining)
        current_search = DLS(data.matrix, data.matrix_size, data.start_point, data.end_point, depth, data.min)
        current_search_result = current_search[0]
        successful = current_search_result.successful
        remaining_nodes = current_search[1]
        depth += 1
        total_nodes_expanded += current_search_result.nodes_expanded
        min_depth = min_depth if current_search_result.min_depth >= min_depth else current_search_result.min_depth
        total_depth += current_search_result.avg_depth  # stored total_depth in avg_depth for DLS only instead of creating another field
    end_time = time.process_time()
    runtime = round(end_time - start_time, 2)
    result = current_search[0]
    result.set_time(runtime)
    result.min_depth = min_depth
    result.nodes_expanded = total_nodes_expanded
    result.EBF = round(total_nodes_expanded ** (1 / depth), 2)
    result.penetration = round(depth / total_nodes_expanded, 2)
    result.avg_depth = round(total_depth / total_nodes_expanded, 2)
    return result
