from dataStructures import *
from Heuristics import *
from numpy import ndarray
import time
import sys
from commonFunctions import *


def ida_star(data: DataInput, h_function, overall_stats: StatsContainer):
    overall_stats.start_time = time.process_time()
    overall_stats.min_depth = data.matrix_size ** 2
    result = AlgorithmResult()
    root = Node(data.start_point, data.matrix[data.start_point.x][data.start_point.y])
    f_limit = h_function(root.coordinates, data.end_point)
    while 1:
        goal, f_limit, overall_stats = dfs_contour(data, root, f_limit, h_function, overall_stats, root.heuristic_value)
        if goal is not None or f_limit == sys.maxsize:
            overall_stats.end_time = time.process_time()
            result.accumulate_stats(overall_stats)
            if result.min_depth == data.matrix_size ** 2:
                result.min_depth = result.max_depth
            if goal is not None:
                result.final_path = goal.path_to_node[:-1]
                result.path_cost = goal.g_cost_of_path
                result.successful = True
            return result


def dfs_contour(data: DataInput, node, f_limit, h_function, stats: StatsContainer, const_fix):
    next_f = sys.maxsize

    if node.f_cost_of_path > f_limit:
        if stats.min_depth > node.depth:
            stats.min_depth = node.depth
        return None, node.f_cost_of_path, stats

    stats.total_depth += node.depth
    if node.coordinates == data.end_point:
        return node, f_limit, stats

    successors = get_children(node, data.matrix, h_function, data.end_point)
    if len(successors) != 0:
        stats.total_nodes_expanded += 1
        stats.total_h += node.heuristic_value
    elif stats.min_depth > node.depth:
        stats.min_depth = node.depth

    for successor in successors:
        if successor.depth > stats.max_depth:
            stats.max_depth = successor.depth
        if successor.coordinates in node.list_of_cords:
            continue
        solution, new_f, stats = dfs_contour(data, successor, f_limit, h_function, stats, const_fix)
        if solution is not None:
            return solution, f_limit, stats
        next_f = min(next_f, new_f)
    return None, next_f, stats