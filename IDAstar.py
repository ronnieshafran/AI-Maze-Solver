from dataStructures import *
from Heuristics import *
from numpy import ndarray
import time
from commonFunctions import *


def ida_star(data: DataInput, h_function, overall_stats: StatsContainer) -> AlgorithmResult:
    overall_stats.start_time = time.process_time()
    root = Node(data.start_point, data.matrix[data.start_point.x][data.start_point.y])
    f_limit = root.f_cost_of_path
    while 1:
        goal, f_limit, overall_stats = dfs_contour(data, root, f_limit, h_function)
        if goal is not None or f_limit == float('inf'):
            if goal is not None:
                overall_stats.end_time = time.process_time()
                return goal.path_to_node[:-1]


#    end_time = time.process_time()
#    runtime = round(end_time - start_time, 2)
#    result = current_search[0]
#    result.set_time(runtime)
#    result.nodes_expanded = total_nodes_expanded
#    result.EBF = round(total_nodes_expanded ** (1 / depth), 2)
#    result.penetration = round(depth / total_nodes_expanded, 2)
#    result.avg_depth = round(total_depth / total_nodes_expanded, 2)


def dfs_contour(data: DataInput, node: Node, f_limit, h_function, stats: StatsContainer):
    if not hasattr(dfs_contour, "next_f"):
        dfs_contour.next_f = float('inf')
    if node.f_cost_of_path > f_limit:
        return None, node.f_cost_of_path, stats
    if node.coordinates == data.end_point:
        return node, f_limit, stats

    successors = get_children(node, data.matrix, h_function, data.end_point)
    for successor in successors:
        if successor.depth > stats.max_depth:
            stats.max_depth = successor.depth
        solution, new_f = dfs_contour(data, successor, f_limit, h_function, next_f)
        if solution is not None:
            return solution, f_limit, stats
        next_f = min(next_f, new_f)
    return None, next_f, stats
