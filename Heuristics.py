from math import sqrt


def euclidean_distance(node_coordinates, end_point):
    x_delta = end_point.x - node_coordinates.x
    y_delta = end_point.y - node_coordinates.y
    return sqrt(x_delta ** 2 + y_delta ** 2)


def manhattan_distance(node_coordinates, end_point):
    horizontal = abs(end_point.x - node_coordinates.x)
    vertical = abs(end_point.y - node_coordinates.y)
    return horizontal + vertical


def max_heuristic(node_coordinates, end_point):
    euclidean = euclidean_distance(node_coordinates, end_point)
    manhattan = manhattan_distance(node_coordinates, end_point)
    return max(euclidean, manhattan)


def zero_heuristic(node_coordinates, end_point):
    return 0
