from math import sqrt


def euclidean_distance(node_coordinates, end_point, min_value):
    x_delta = end_point.x - node_coordinates.x
    y_delta = end_point.y - node_coordinates.y
    return (sqrt(x_delta ** 2 + y_delta ** 2) / sqrt(2)) * min_value


def chebyshev_distance(node_coordinates, end_point, min_value):
    x_delta = abs(end_point.x - node_coordinates.x)
    y_delta = abs(end_point.y - node_coordinates.y)
    return max(x_delta, y_delta) * min_value


def zero_heuristic(node_coordinates, end_point, min_value):
    return 0
