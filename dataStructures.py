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

    @property
    def queue(self):
        return self._queue


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
        return self.x, self.y

    def __hash__(self):
        return hash(self.__key())


class DataInput:
    def __init__(self, selected_algorithm, matrix_size, start_point, end_point, matrix, min_value):
        self.matrix = matrix
        self.end_point = end_point
        self.start_point = start_point
        self.matrix_size = matrix_size
        self.selected_algorithm = selected_algorithm
        self.min = min_value


class StatsContainer:
    def __init__(self, start_time=0.0, end_time=0.0, total_depth=0, total_nodes_expanded=0, total_h=0,
                 min_depth=0, max_depth=0):
        self.start_time = start_time
        self.end_time = end_time
        self.total_depth = total_depth
        self.total_nodes_expanded = total_nodes_expanded
        self.total_h = total_h
        self.min_depth = min_depth
        self.max_depth = max_depth


class AlgorithmResult:
    def __init__(self, final_path="", path_cost=0, nodes_expanded=0, penetration=0, successful=0, EBF=0.0, avg_H=0,
                 min_depth=0,
                 max_depth=0, avg_depth=0, time=0):
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
        self.time = time

    # could be expanded to more stats
    def accumulate_stats_for_iterative_algorithms(self, other):
        self.nodes_expanded += other.nodes_expanded

    def accumulate_stats(self, stats: StatsContainer()):
        self.max_depth = stats.max_depth
        self.avg_depth = round(stats.total_depth / stats.total_nodes_expanded, 2)
        self.min_depth = stats.min_depth
        self.avg_H = round(stats.total_h / stats.total_nodes_expanded, 2)
        self.EBF = round(stats.total_nodes_expanded ** (1 / stats.max_depth), 2)
        self.penetration = round(stats.max_depth / stats.total_nodes_expanded, 2)
        self.nodes_expanded = stats.total_nodes_expanded
        self.time = stats.end_time - stats.start_time

    def __str__(self):
        return f'successful: {self.successful} \n' \
               f'final path: {self.final_path} \n' \
               f'final cost: {self.path_cost} \n' \
               f'nodes expanded: {self.nodes_expanded} \n' \
               f'max depth: {self.max_depth} \n' \
               f'min depth: {self.min_depth} \n' \
               f'avg depth: {self.avg_depth} \n' \
               f'***FOR INFORMED SEARCHES: \n' \
               f'EBF: {self.EBF} \n' \
               f'avg H: {self.avg_H} \n' \
               f'dN: {self.penetration} \n' \
               f'runtime: {self.time}'

    def set_time(self, time):
        self.time = time


class Node:
    def __init__(self, coordinates=Point([0, 0]), cost=-1, path_to_node='', depth=0, g_cost_of_path=0,
                 heuristic_value=0,
                 f_cost_of_path=0, list_of_cords=[]):
        self.g_cost_of_path = g_cost_of_path
        self.heuristic_value = heuristic_value
        self.path_to_node = path_to_node
        self.depth = depth
        self.cost = cost
        self.coordinates = coordinates
        self.f_cost_of_path = f_cost_of_path
        self.list_of_cords = list_of_cords
