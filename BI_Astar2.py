from commonFunctions import *


def run(data: DataInput, h_function) -> AlgorithmResult:
    # In this algorithm we use 2 Priority Queues, which are used to maintain minimum values in order
    # in both forward and backward iterations. Queues are called: forward_open_queue, backward_open_queue.
    # We also use 2 Dictionaries, which are used to maintain the visited list of nodes
    # in both forward and backward iterations. Dictionaries are called: forward_visited, backward_open_queue.
    # ------- variables used to calculate stats ------- #
    start_time = time.process_time()
    success = False
    max_depth = 0
    min_depth = 0
    total_h = 0
    total_depth = 0
    total_expanded_nodes = 0
    # ------- End of variables used to calculate stats ------- #
    root = Node(data.start_point, data.matrix[data.start_point.x][data.start_point.y])
    goal = Node(data.end_point, data.matrix[data.end_point.x][data.end_point.y])
    goal.g_cost_of_path = goal.cost
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
        if not forward_open_queue.is_empty():
            current_forward_node = forward_open_queue.remove()
            if (current_forward_node.coordinates == goal.coordinates) or (current_forward_node in backward_open_queue.queue):
                goal_forward = current_forward_node
                success = True
                if current_forward_node.coordinates == goal.coordinates:
                    goal_backward = None
                elif current_forward_node in backward_open_queue:
                    goal_backward = backward_open_queue.queue.remove(current_forward_node)
                    backward_open_queue.queue.sort()
                break

            forward_visited |= {current_forward_node.coordinates: current_forward_node}
            forward_nodes_to_enqueue = get_children(current_forward_node, data.matrix, h_function, data.end_point)

            for node in forward_nodes_to_enqueue:
                if node.coordinates not in forward_visited:
                    forward_open_queue.insert(node, node.f_cost_of_path)

                elif node.f_cost_of_path < forward_visited.get(node.coordinates).f_cost_of_path:
                    forward_visited.pop(node.coordinates)
                    forward_open_queue.insert(node, node.f_cost_of_path)

        # --------------------- Done with forward iteration --------------------- #

        elif not backward_open_queue.is_empty():
            current_backward_node = backward_open_queue.remove()
            if (current_backward_node.coordinates == goal.coordinates) or (current_backward_node in forward_open_queue.queue):
                goal_backward = current_backward_node
                success = True
                if current_backward_node.coordinates == goal.coordinates:
                    goal_forward = None
                elif current_backward_node in forward_open_queue:
                    goal_forward = forward_open_queue.queue.remove(current_backward_node)
                    forward_open_queue.queue.sort()
                break

            backward_visited |= {current_backward_node.coordinates: current_backward_node}
            backward_nodes_to_enqueue = get_children(current_backward_node, data.matrix, h_function, data.end_point)

            for node in backward_nodes_to_enqueue:
                if node.coordinates not in backward_visited:
                    backward_open_queue.insert(node, node.f_cost_of_path)

                elif node.f_cost_of_path < backward_visited.get(node.coordinates).f_cost_of_path:
                    backward_visited.pop(node.coordinates)
                    backward_open_queue.insert(node, node.f_cost_of_path)
        else:
            success = False

    runtime = time.process_time()
    print(runtime-start_time)
    if success:
        if (goal_forward is not None) and (goal_backward is not None):
            optimal_path, min_val = (find_optimal_path(goal_forward, goal_backward, forward_visited,
                                                       backward_visited, forward_open_queue.queue,
                                                       backward_open_queue.queue, root.cost))
            if min_val < goal_forward.g_cost_of_path + goal_backward.g_cost_of_path - goal_backward.cost:
                goal_forward = optimal_path[0]
                goal_backward = optimal_path[1]
            print(fix_path(goal_forward, False)+fix_path(goal_backward, True), goal_backward.g_cost_of_path)
        elif (goal_backward is not None) and (goal_forward is None):
            print(fix_path(goal_backward, True), goal_backward.g_cost_of_path)
        elif (goal_forward is not None) and (goal_backward is None):
            print(fix_path(goal_forward, False), goal_forward.g_cost_of_path)
    else:
        print("failed")
        return None


def find_optimal_path(forward: Node(), backward: Node(), visited_forward: {}, visited_backward: {},
                      open_forward: [], open_backward: [], root_cost):
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

    return optimal_path, min_val


def fix_path(node: Node(), all_backward):
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
