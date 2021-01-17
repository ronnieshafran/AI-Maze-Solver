from commonFunctions import *
from dataStructures import *
from math import log2
from sys import maxsize
import time


def run(data: DataInput, h_function, start_time, total_runtime=0) -> AlgorithmResult:
    # In this algorithm we use 2 Priority Queues, which are used to maintain minimum values in order
    # in both forward and backward iterations. Queues are called: forward_open_queue, backward_open_queue.
    # We also use 2 Dictionaries, which are used to maintain the visited list of nodes
    # in both forward and backward iterations. Dictionaries are called: forward_visited, backward_open_queue.
    # ------- variables used to calculate stats ------- #
    total_runtime = total_runtime if total_runtime > 0 else round(log2(data.matrix_size), 2)
    out_of_time = False
    max_depth = 0
    min_depth = maxsize
    total_depth = 0
    total_h = 0
    total_expanded_nodes = 0
    total_attempts = 0
    # ------- End of variables used to calculate stats ------- #
    root = Node(data.start_point, data.matrix[data.start_point.x][data.start_point.y])
    goal = Node(data.end_point, data.matrix[data.end_point.x][data.end_point.y])
    goal.g_cost_of_path = goal.cost
    goal_depth = goal.depth
    forward_visited = {root.coordinates: root}
    backward_visited = {goal.coordinates: goal}
    forward_open_queue = PriorityQueue()
    backward_open_queue = PriorityQueue()
    forward_open_queue.insert(root, 0)
    backward_open_queue.insert(goal, goal.cost)
    goal_forward = None
    goal_backward = None

    # ------- actual algorithm, as studied in lectures, plus stats calculations ------- #
    while (not forward_open_queue.is_empty()) and (not backward_open_queue.is_empty()):
        current_time = time.process_time()
        if current_time - start_time >= total_runtime:
            print("Out of time!")
            out_of_time = True
            break

        if not forward_open_queue.is_empty():
            current_forward_node = forward_open_queue.remove()

            if (current_forward_node.coordinates == goal.coordinates) or (current_forward_node in
                                                                          backward_open_queue.queue):
                # goal was found or forward and backward clashed
                goal_forward = current_forward_node
                if current_forward_node.coordinates == goal.coordinates:
                    # goal was found in forward iteration
                    goal_backward = None
                elif current_forward_node in backward_open_queue:
                    # forward and backward clashed
                    goal_backward = backward_open_queue.queue.remove(current_forward_node)
                    backward_open_queue.queue.sort()
                max_depth, min_depth, total_attempts, total_depth = \
                    calculate_depth_stats_on_cutoff(current_forward_node, max_depth, min_depth,
                                                    total_attempts, total_depth)
                break

            total_expanded_nodes += 1
            total_h += current_forward_node.heuristic_value

            forward_visited |= {current_forward_node.coordinates: current_forward_node}
            forward_nodes_to_enqueue = get_children(current_forward_node, data.matrix,
                                                    h_function, data.end_point, data.min)

            nodes_enqueued = 0
            # forward cutoff
            if len(forward_nodes_to_enqueue) == 0:
                max_depth, min_depth, total_attempts, total_depth = \
                    calculate_depth_stats_on_cutoff(current_forward_node, max_depth, min_depth, total_attempts,
                                                    total_depth)
            else:
                for node in forward_nodes_to_enqueue:
                    if node.coordinates not in forward_visited:
                        nodes_enqueued += 1
                        forward_open_queue.insert(node, node.f_cost_of_path)

                    elif node.f_cost_of_path < forward_visited.get(node.coordinates).f_cost_of_path:
                        nodes_enqueued += 1
                        forward_visited.pop(node.coordinates)
                        forward_open_queue.insert(node, node.f_cost_of_path)

            if nodes_enqueued == 0:
                max_depth, min_depth, total_attempts, total_depth = \
                    calculate_depth_stats_on_cutoff(current_forward_node, max_depth, min_depth, total_attempts,
                                                    total_depth)

        # ----------------- Done with forward iteration ----------------- #

        if not backward_open_queue.is_empty():
            current_backward_node = backward_open_queue.remove()
            if (current_backward_node.coordinates == goal.coordinates) or (current_backward_node in
                                                                           forward_open_queue.queue):
                # goal was found or forward and backward clashed
                goal_backward = current_backward_node
                if current_backward_node.coordinates == goal.coordinates:
                    # goal was found in backward iteration
                    goal_forward = None
                    max_depth, min_depth, total_attempts, total_depth = \
                        calculate_depth_stats_on_cutoff(current_backward_node, max_depth, min_depth, total_attempts,
                                                        total_depth, goal_depth)
                elif current_backward_node in forward_open_queue:
                    # forward and backward clashed
                    goal_forward = forward_open_queue.queue.remove(current_backward_node)
                    forward_open_queue.queue.sort()
                break

            total_expanded_nodes += 1
            total_h += current_backward_node.heuristic_value

            backward_visited |= {current_backward_node.coordinates: current_backward_node}
            backward_nodes_to_enqueue = get_children(current_backward_node, data.matrix, h_function, data.end_point)

            nodes_enqueued = 0
            # backward cutoff
            if len(backward_nodes_to_enqueue) == 0:
                max_depth, min_depth, total_attempts, total_depth = \
                    calculate_depth_stats_on_cutoff(current_backward_node, max_depth, min_depth, total_attempts,
                                                    total_depth, goal_depth)
            else:
                for node in backward_nodes_to_enqueue:
                    if node.coordinates not in backward_visited:
                        nodes_enqueued += 1
                        backward_open_queue.insert(node, node.f_cost_of_path)

                    elif node.f_cost_of_path < backward_visited.get(node.coordinates).f_cost_of_path:
                        nodes_enqueued += 1
                        backward_visited.pop(node.coordinates)
                        backward_open_queue.insert(node, node.f_cost_of_path)

            if nodes_enqueued == 0:
                max_depth, min_depth, total_attempts, total_depth = \
                    calculate_depth_stats_on_cutoff(current_backward_node, max_depth, min_depth, total_attempts,
                                                    total_depth, goal_depth)

    # determine final depth for EBF / d/N stats
    final_depth = get_final_depth(goal_forward, goal_backward, goal_depth, max_depth)

    # calculation of final stats
    if out_of_time:
        final_depth, total_attempts, total_depth = calc_stats_if_out_of_time(final_depth, total_attempts, total_depth)

    EBF, avg_depth, avg_h, min_depth, penetration = \
        calc_final_stats(final_depth, max_depth, min_depth, total_attempts, total_depth,
                         total_expanded_nodes, total_h)
    end_time = time.process_time()
    total_runtime = round(end_time - start_time, 4)
    if (goal_forward is not None) or (goal_backward is not None):
        fixed_path = ''
        final_g_cost = 0
        if (goal_forward is not None) and (goal_backward is not None):
            optimal_path, min_val = (find_optimal_path(goal_forward, goal_backward, forward_visited,
                                                       backward_visited, forward_open_queue.queue,
                                                       backward_open_queue.queue))
            if min_val < goal_forward.g_cost_of_path + goal_backward.g_cost_of_path - goal_backward.cost:
                goal_forward = optimal_path[0]
                goal_backward = optimal_path[1]
            final_g_cost = goal_forward.g_cost_of_path + goal_backward.g_cost_of_path - goal_backward.cost
            fixed_path = goal_forward.path_to_node[:-1] + fix_path(goal_backward, False)
        elif goal_forward is not None:
            final_g_cost = goal_forward.g_cost_of_path
            fixed_path = goal_forward.path_to_node[:-1]
        elif goal_backward is not None:
            final_g_cost = goal_backward.g_cost_of_path
            fixed_path = fix_path(goal_backward, True)

        return AlgorithmResult(fixed_path, final_g_cost, total_expanded_nodes, penetration, True,
                               EBF, avg_h, min_depth, max_depth, avg_depth, total_runtime)

    else:
        return AlgorithmResult("", 0, total_expanded_nodes, penetration, False, EBF, avg_h, min_depth, max_depth,
                               avg_depth, total_runtime)


def find_optimal_path(forward: Node(), backward: Node(), visited_forward: {}, visited_backward: {},
                      open_forward: [], open_backward: []):
    optimal_path = (forward, backward)
    min_val = forward.g_cost_of_path + backward.g_cost_of_path - forward.cost

    for node in visited_forward:
        forward_node = visited_forward[node]
        if node in visited_backward:
            backward_node = visited_backward.get(node)
            g_cost_forward = forward_node.g_cost_of_path
            g_cost_backward = backward_node.g_cost_of_path
            if g_cost_backward + g_cost_forward - backward_node.cost < min_val:
                min_val = g_cost_backward + g_cost_forward - backward_node.cost
                optimal_path = (forward_node, backward_node)

    for node in open_forward:
        forward_node = open_forward[node]
        if node in open_backward:
            backward_node = open_backward.get(node)
            g_cost_forward = forward_node.g_cost_of_path
            g_cost_backward = backward_node.g_cost_of_path
            if g_cost_backward + g_cost_forward - backward_node.cost < min_val:
                min_val = g_cost_backward + g_cost_forward - backward_node.cost
                optimal_path = (forward_node, backward_node)

    for node in open_forward:
        forward_node = open_forward[node]
        if node in visited_backward:
            backward_node = visited_backward.get(node)
            g_cost_forward = forward_node.g_cost_of_path
            g_cost_backward = backward_node.g_cost_of_path
            if g_cost_backward + g_cost_forward - backward_node.cost < min_val:
                min_val = g_cost_backward + g_cost_forward - backward_node.cost
                optimal_path = (forward_node, backward_node)

    for node in visited_forward:
        forward_node = visited_forward[node]
        if node in open_backward:
            backward_node = open_backward.get(node)
            g_cost_forward = forward_node.g_cost_of_path
            g_cost_backward = backward_node.g_cost_of_path
            if g_cost_backward + g_cost_forward - backward_node.cost < min_val:
                min_val = g_cost_backward + g_cost_forward - backward_node.cost
                optimal_path = (forward_node, backward_node)

    return optimal_path, min_val


def fix_path(node: Node(), all_backward):
    if node is None:
        return ''

    path = node.list_of_cords[::-1]
    path.insert(0, node.coordinates)
    fixed_path = ''

    for index in range(len(path) - 1):
        if path[index].x + 1 == path[index + 1].x and path[index].y + 1 == path[index + 1].y:
            if not all_backward:
                fixed_path += "-RD"
            else:
                fixed_path += "RD"
        elif path[index].x + 1 == path[index + 1].x and path[index].y == path[index + 1].y:
            if not all_backward:
                fixed_path += "-D"
            else:
                fixed_path += "D"
        elif path[index].x + 1 == path[index + 1].x and path[index].y - 1 == path[index + 1].y:
            if not all_backward:
                fixed_path += "-LD"
            else:
                fixed_path += "LD"
        elif path[index].x == path[index + 1].x and path[index].y - 1 == path[index + 1].y:
            if not all_backward:
                fixed_path += "-L"
            else:
                fixed_path += "L"
        elif path[index].x - 1 == path[index + 1].x and path[index].y - 1 == path[index + 1].y:
            if not all_backward:
                fixed_path += "-LU"
            else:
                fixed_path += "LU"
        elif path[index].x - 1 == path[index + 1].x and path[index].y == path[index + 1].y:
            if not all_backward:
                fixed_path += "-U"
            else:
                fixed_path += "U"
        elif path[index].x - 1 == path[index + 1].x and path[index].y + 1 == path[index + 1].y:
            if not all_backward:
                fixed_path += "-RU"
            else:
                fixed_path += "RU"
        elif path[index].x == path[index + 1].x and path[index].y + 1 == path[index + 1].y:
            if not all_backward:
                fixed_path += "-R"
            else:
                fixed_path += "R"
        if all_backward and index != len(path) - 2:
            fixed_path += "-"
    return fixed_path


def calc_final_stats(final_depth, max_depth, min_depth, total_attempts, total_depth, total_expanded_nodes, total_h):
    avg_depth = round(total_depth / total_attempts, 2)
    avg_h = round(total_h / total_expanded_nodes, 2)
    EBF = round(total_expanded_nodes ** (1 / final_depth), 2)
    penetration = round(final_depth / total_expanded_nodes, 2)
    min_depth = max_depth if min_depth == maxsize else min_depth
    return EBF, avg_depth, avg_h, min_depth, penetration


def get_final_depth(goal_forward, goal_backward, goal_depth, max_depth):
    if (goal_backward is None) and (not (goal_forward is None)):
        # goal was found in forward iteration
        final_depth = goal_forward.depth
    elif (goal_forward is None) and (not (goal_backward is None)):
        # goal was found in backward iteration
        final_depth = goal_depth - goal_backward.depth
    elif not ((goal_forward is None) and (goal_backward is None)):
        # goal was found in open list
        final_depth = goal_forward.depth
    else:
        final_depth = max_depth
    return final_depth


def calc_stats_if_out_of_time(final_depth, total_attempts, total_depth):
    if total_attempts == 0:
        total_attempts = 1
        total_depth = 0
    if final_depth == 0:
        final_depth = 1
    return final_depth, total_attempts, total_depth


def calculate_depth_stats_on_cutoff(current_node, max_depth, min_depth, total_attempts, total_depth, goal_depth=0):
    if goal_depth == 0:
        # calculated in forward iteration
        current_depth = current_node.depth
    else:
        # calculated in backward iteration
        current_depth = goal_depth - current_node.depth

    if current_depth > max_depth:
        max_depth = current_depth
    if current_depth < min_depth:
        min_depth = current_depth

    total_depth += current_depth
    total_attempts += 1
    return max_depth, min_depth, total_attempts, total_depth
