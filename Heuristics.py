from math import sqrt


def euclidean_distance(node_coordinates, end_point):
    x_delta = end_point.x - node_coordinates.x
    y_delta = end_point.y - node_coordinates.y
    return sqrt(x_delta ** 2 + y_delta ** 2)


def zero_heuristic(node_coordinates, end_point):
    return 0
