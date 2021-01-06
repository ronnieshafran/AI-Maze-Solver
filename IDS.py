import time

from dataStructures import *
from queue import LifoQueue
from commonFunctions import get_children
from sys import maxsize


def DLS(matrix, start_point, end_point, search_depth) -> (AlgorithmResult, bool, int, int):
    stack = LifoQueue()
    observed_points_set = set()
    total_expanded_nodes = 0
    min_depth = maxsize
    max_depth = 0
    total_depth = 0
    start_node = Node(start_point, matrix[start_point.x][start_point.y])
    goal_node = None
    remaining_nodes = False
    total_attempts = 0

    stack.put(start_node)
    observed_points_set.add(start_node.coordinates)
    while not stack.empty():

        current_node = stack.get()

        if current_node.coordinates == end_point:
            min_depth, total_attempts, total_depth, max_depth = update_stats_when_cutoff(current_node, min_depth, max_depth, total_attempts, total_depth)
            goal_node = current_node
            break

        if current_node.depth >= search_depth:
            remaining_nodes = True
            min_depth, total_attempts, total_depth, max_depth = update_stats_when_cutoff(current_node, min_depth, max_depth, total_attempts, total_depth)
            continue

        max_depth = current_node.depth if current_node.depth > max_depth else max_depth
        total_expanded_nodes += 1
        observed_points_set.add(current_node.coordinates)
        children_nodes = get_children(current_node, matrix)
        children_nodes.reverse()

        if len(children_nodes) == 0:
            min_depth, total_attempts, total_depth, max_depth = update_stats_when_cutoff(current_node, min_depth, max_depth, total_attempts, total_depth)

        for node in children_nodes:
            if node.coordinates in observed_points_set:
                continue
            else:
                stack.put(node)

    if goal_node is not None:
        return (AlgorithmResult(goal_node.path_to_node[:-1], goal_node.g_cost_of_path, total_expanded_nodes, 0, True, 0, 0,
                                min_depth, max_depth, 0), remaining_nodes, total_depth, total_attempts)
    else:
        return AlgorithmResult("", 0, total_expanded_nodes, 0, False, 0, 0, min_depth, max_depth, 0), remaining_nodes, total_depth, total_attempts


def update_stats_when_cutoff(current_node, min_depth, max_depth, total_attempts, total_depth):
    max_depth = current_node.depth if current_node.depth > max_depth else max_depth
    total_depth += current_node.depth
    total_attempts += 1
    min_depth = current_node.depth if current_node.depth < min_depth else min_depth
    return min_depth, total_attempts, total_depth, max_depth


def run(data: DataInput) -> AlgorithmResult:
    start_time = time.process_time()
    current_search = None
    depth = 0
    remaining_nodes = True
    successful = False
    total_nodes_expanded = 0
    total_depth = 0
    total_attempts = 0
    min_depth = maxsize
    while remaining_nodes and not successful:
        # current_search returns tuple: (AlgorithmResult result, boolean remaining, int total_depth, int total_attempts)
        current_search = DLS(data.matrix, data.start_point, data.end_point, depth)
        successful = current_search[0].successful
        remaining_nodes = current_search[1]
        depth += 1
        total_nodes_expanded += current_search[0].nodes_expanded
        total_depth += current_search[2]
        total_attempts += current_search[3]
        min_depth = current_search[0].min_depth if current_search[0].min_depth < min_depth else min_depth
    end_time = time.process_time()
    runtime = round(end_time - start_time, 2)
    result = current_search[0]
    result.set_time(runtime)
    result.min_depth = min_depth
    result.nodes_expanded = total_nodes_expanded
    result.EBF = round(total_nodes_expanded ** (1 / depth), 2)
    result.penetration = round(depth / total_nodes_expanded, 2)
    result.avg_depth = round(total_depth / total_attempts, 2)
    return result
