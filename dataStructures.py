import heapq


class PriorityQueue:

    def __init__(self):
        self._queue = []
        self._index = 0

    def insert(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def remove(self):
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        return len(self._queue) == 0


class Point:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __key(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.__key())


class DataInput:
    def __init__(self, selected_algorithm, matrix_size, start_point, end_point, matrix):
        self.matrix = matrix
        self.end_point = end_point
        self.start_point = start_point
        self.matrix_size = matrix_size
        self.selected_algorithm = selected_algorithm


class AlgorithmResult:
    def __init__(self, final_path, path_cost, nodes_expanded, penetration, successful, EBF, avg_H, min_depth, max_depth,
                 avg_depth):
        self.max_depth = max_depth
        self.avg_depth = avg_depth
        self.min_depth = min_depth
        self.avg_H = avg_H
        self.EBF = EBF
        self.successful = successful
        self.penetration = penetration
        self.nodes_expanded = nodes_expanded
        self.path_cost = path_cost
        self.final_path = final_path

    def __str__(self):
        if self.successful:
            return f'final path: {self.final_path} \n' \
               f'final cost: {self.path_cost} \n' \
               f'nodes expanded: {self.nodes_expanded} \n' \
               f'max depth: {self.max_depth} \n' \
               f'min depth: {self.min_depth} \n' \
               f'***FOR INFORMED SEARCHES: \n' \
               f'EBF: {self.EBF} \n' \
               f'avg H: {self.avg_H} \n' \
               f'penetration: {self.penetration}'
        else:
            return 'Algorithm Failed!'


class Node:
    def __init__(self, coordinates=Point([0, 0]), cost=-1, path_to_node='', depth=0, cost_of_path=0, heuristic_value=0, g_cost_of_path = 0):
        self.g_cost_of_path = g_cost_of_path
        self.heuristic_value = heuristic_value
        self.path_to_node = path_to_node
        self.depth = depth
        self.cost = cost
        self.coordinates = coordinates
        self.f_cost_of_path = cost_of_path


