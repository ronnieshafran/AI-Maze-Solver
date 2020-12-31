from dataStructures import *
from Heuristics import *
from numpy import ndarray
import time
import sys
from commonFunctions import *


def ida_star(data: DataInput, h_function, overall_stats: StatsContainer):
    path = []
    overall_stats.start_time = time.process_time()
    root = Node(data.start_point, data.matrix[data.start_point.x][data.start_point.y])
    path.append(root)
    f_limit = root.f_cost_of_path
    while 1:
        goal, f_limit, overall_stats = dfs_contour(data, path, f_limit, h_function, overall_stats)
        if goal is not None:
            overall_stats.end_time = time.process_time()
            return goal.path_to_node[:-1]
        if f_limit == sys.maxsize:
            return ''
        if time.process_time() > 20:
            return


#    end_time = time.process_time()
#    runtime = round(end_time - start_time, 2)
#    result = current_search[0]
#    result.set_time(runtime)
#    result.nodes_expanded = total_nodes_expanded
#    result.EBF = round(total_nodes_expanded ** (1 / depth), 2)
#    result.penetration = round(depth / total_nodes_expanded, 2)
#    result.avg_depth = round(total_depth / total_nodes_expanded, 2)


def dfs_contour(data: DataInput, path, f_limit, h_function, stats: StatsContainer):
    if not hasattr(dfs_contour, "next_f"):
        dfs_contour.next_f = sys.maxsize

    node = path[-1]
    if node.f_cost_of_path > f_limit:
        return None, node.f_cost_of_path, stats
    if node.coordinates == data.end_point:
        stats.success = 'Y'
        return node, f_limit, stats

    successors = get_children(node, data.matrix, h_function, data.end_point)
    for successor in successors:
        if successor.depth > stats.max_depth:
            stats.max_depth = successor.depth
        if successor not in path:
            path.append(successor)
            solution, new_f, stats = dfs_contour(data, path, f_limit, h_function, stats)
            if solution is not None:
                return solution, new_f, stats
            dfs_contour.next_f = min(dfs_contour.next_f, new_f)
            path.remove(successor)
    return None, dfs_contour.next_f, stats
