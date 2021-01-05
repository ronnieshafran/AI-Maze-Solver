from math import sqrt
from math import floor


def euclidean_distance(node_coordinates, end_point):
    x_delta = end_point.x - node_coordinates.x
    y_delta = end_point.y - node_coordinates.y
    return sqrt(x_delta ** 2 + y_delta ** 2)


def manhattan_distance(node_coordinates, end_point):
    x_delta = abs(end_point.x - node_coordinates.x)
    y_delta = abs(end_point.y - node_coordinates.y)
    return x_delta + y_delta


def manhattan_avg(node_coordinates, end_point):
    x_delta = abs(end_point.x - node_coordinates.x)
    y_delta = abs(end_point.y - node_coordinates.y)
    return floor((x_delta + y_delta) / 2)


def octile_distance(node_coordinates, end_point):
    x_delta = abs(end_point.x - node_coordinates.x)
    y_delta = abs(end_point.y - node_coordinates.y)
    return max(x_delta, y_delta) + ((sqrt(2) - 1) * min(x_delta, y_delta))


def zero_heuristic(node_coordinates, end_point):
    return 0
