from dataStructures import *
from commonFunctions import *
from Heuristics import octile_distance
from numpy import ndarray
import time


def run(data: DataInput, h_function) -> AlgorithmResult:
    start_time = time.process_time()
    forward_open_queue = PriorityQueue()
    backward_open_queue = PriorityQueue()
    forward_visited = {}
    backward_visited = {}
    root = Node(data.start_point, data.matrix[data.start_point.x][data.start_point.y])
    goal = Node(data.end_point, data.matrix[data.end_point.x][data.end_point.y])
    goal_forward = Node()
    goal_backward = Node()
    forward_open_queue.insert(root, 0)
    backward_open_queue.insert(goal, 0)
    max_depth = 0
    min_depth = 0
    total_h = 0
    total_depth = 0

    while not (forward_open_queue.is_empty() and backward_open_queue.is_empty()):
        current_forward_node = forward_open_queue.remove()
        current_backward_node = backward_open_queue.remove()

        if current_forward_node.coordinates in forward_visited and current_forward_node.f_cost_of_path >= \
                forward_visited.get(current_forward_node.coordinates).f_cost_of_path:
            continue

        if current_backward_node.coordinates in backward_visited and current_backward_node.f_cost_of_path >= \
                backward_visited.get(current_backward_node.coordinates).f_cost_of_path:
            continue

        # statistics calculation
        if current_forward_node.depth > max_depth:
            max_depth = current_forward_node.depth
        if goal.depth - current_backward_node.depth > max_depth:
            max_depth = goal.depth - current_backward_node.depth

        total_depth += current_forward_node.depth + goal.depth - current_backward_node.depth
        total_h += current_forward_node.heuristic_value + current_backward_node.heuristic_value

        if current_forward_node.coordinates == current_backward_node.coordinates:
            goal_forward = current_forward_node
            goal_backward = current_backward_node
            break

        forward_visited |= {current_forward_node.coordinates: current_forward_node}
        forward_nodes_to_enqueue = get_children(current_forward_node, data.matrix, h_function, data.end_point)

        backward_visited |= {current_backward_node.coordinates: current_backward_node}
        backward_nodes_to_enqueue = get_children(current_backward_node, data.matrix, h_function, data.start_point)

        # check for min depth when the search path is "stuck"
        if len(forward_nodes_to_enqueue) == 0 and min_depth > current_forward_node.depth:
            min_depth = current_forward_node.depth
        if len(backward_nodes_to_enqueue) == 0 and min_depth > goal.depth - current_backward_node.depth:
            min_depth = goal.depth - current_backward_node.depth

        else:
            for node in forward_nodes_to_enqueue:
                if node.coordinates not in forward_visited:
                    forward_open_queue.insert(node, node.f_cost_of_path)

                elif node.f_cost_of_path < forward_visited.get(node.coordinates).f_cost_of_path:
                    forward_visited.pop(node.coordinates)
                    forward_open_queue.insert(node, node.f_cost_of_path)

            for node in backward_nodes_to_enqueue:
                if node.coordinates not in backward_visited:
                    backward_open_queue.insert(node, node.f_cost_of_path)

                elif node.f_cost_of_path < backward_visited.get(node.coordinates).f_cost_of_path:
                    backward_visited.pop(node.coordinates)
                    backward_open_queue.insert(node, node.f_cost_of_path)

    # stats calculation, needs to be updated for this algorithm.
    total_expanded_nodes = len(forward_visited) + len(backward_visited)
    avg_depth = round(total_depth / total_expanded_nodes, 2)
    avg_h = round(total_h / total_expanded_nodes, 2)
    EBF = round(total_expanded_nodes ** (1 / max_depth), 2)
    penetration = round(max_depth / total_expanded_nodes, 2)
    min_depth = max_depth if min_depth == data.matrix_size ** 2 else max_depth
    if goal_forward.cost > 0 and goal_backward.cost > 0:
        optimal_path, min_val = (
            find_optimal_path(current_forward_node, current_backward_node, forward_visited, backward_visited,
                              convert_priority_que(forward_open_queue), convert_priority_que(backward_open_queue), root.cost))
        if min_val < goal_forward.g_cost_of_path + goal_backward.g_cost_of_path:
            goal_forward = optimal_path[0]
            goal_backward = optimal_path[1]

        return AlgorithmResult(goal_forward.path_to_node[:-1] + fix_backward_path(goal_backward),
                               min_val, total_expanded_nodes, penetration, True,
                               EBF, avg_h, min_depth, max_depth, avg_depth, time.process_time() - start_time)
    else:
        return AlgorithmResult("", 0, total_expanded_nodes, penetration, False, EBF, avg_h, min_depth, max_depth,
                               avg_depth, time.process_time() - start_time)

    # repeat until queues is empty


def convert_priority_que(que: PriorityQueue()):
    converted_list = {}
    while not que.is_empty():
        node = que.remove()
        converted_list |= {node.coordinates: node}
    return converted_list


def find_optimal_path(forward: Node(), backward: Node(), visited_forward: {}, visited_backward: {},
                      open_forward: {}, open_backward: {}, root_cost):
    optimal_path = ()
    min_val = forward.g_cost_of_path + backward.g_cost_of_path

    for node in visited_forward:
        forward_node = visited_forward[node]
        if node in visited_backward:
            backward_node = visited_backward.get(node)
            g_cost_forward = forward_node.g_cost_of_path
            g_cost_backward = backward_node.g_cost_of_path
            if g_cost_backward + g_cost_forward < min_val:
                min_val = g_cost_backward + g_cost_forward
                optimal_path = (forward_node, backward_node)

    return optimal_path, min_val


def fix_backward_path(node: Node()):
    path = node.list_of_cords[::-1]
    path.insert(0, node.coordinates)
    fixed_path = ''
    for index in range(len(path) - 1):
        if path[index].x + 1 == path[index + 1].x and path[index].y + 1 == path[index + 1].y:
            fixed_path += "-RD"
        elif path[index].x + 1 == path[index + 1].x and path[index].y == path[index + 1].y:
            fixed_path += "-D"
        elif path[index].x + 1 == path[index + 1].x and path[index].y - 1 == path[index + 1].y:
            fixed_path += "-LD"
        elif path[index].x == path[index + 1].x and path[index].y - 1 == path[index + 1].y:
            fixed_path += "-L"
        elif path[index].x - 1 == path[index + 1].x and path[index].y - 1 == path[index + 1].y:
            fixed_path += "-LU"
        elif path[index].x - 1 == path[index + 1].x and path[index].y == path[index + 1].y:
            fixed_path += "-U"
        elif path[index].x - 1 == path[index + 1].x and path[index].y + 1 == path[index + 1].y:
            fixed_path += "-RU"
        elif path[index].x == path[index + 1].x and path[index].y + 1 == path[index + 1].y:
            fixed_path += "-R"
    return fixed_path

