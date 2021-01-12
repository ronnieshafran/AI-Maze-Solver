from dataStructures import *
from Heuristics import *
from numpy import ndarray
import time


def get_node_in_direction(parent_node: Node, direction: str, matrix: ndarray, h_function, end_point, min_value) -> Node:
    next_node_coordinates = None
    next_node_value = None
    try:
        if direction == "RU":
            next_node_coordinates = Point([parent_node.coordinates.x - 1, parent_node.coordinates.y + 1])
            next_node_value = matrix[parent_node.coordinates.x - 1][parent_node.coordinates.y + 1]
        elif direction == "R":
            next_node_coordinates = Point([parent_node.coordinates.x, parent_node.coordinates.y + 1])
            next_node_value = matrix[parent_node.coordinates.x][parent_node.coordinates.y + 1]
        elif direction == "RD":
            next_node_coordinates = Point([parent_node.coordinates.x + 1, parent_node.coordinates.y + 1])
            next_node_value = matrix[parent_node.coordinates.x + 1][parent_node.coordinates.y + 1]
        elif direction == "D":
            next_node_coordinates = Point([parent_node.coordinates.x + 1, parent_node.coordinates.y])
            next_node_value = matrix[parent_node.coordinates.x + 1][parent_node.coordinates.y]
        elif direction == "LD":
            next_node_coordinates = Point([parent_node.coordinates.x + 1, parent_node.coordinates.y - 1])
            next_node_value = matrix[parent_node.coordinates.x + 1][parent_node.coordinates.y - 1]
        elif direction == "L":
            next_node_coordinates = Point([parent_node.coordinates.x, parent_node.coordinates.y - 1])
            next_node_value = matrix[parent_node.coordinates.x][parent_node.coordinates.y - 1]
        elif direction == "LU":
            next_node_coordinates = Point([parent_node.coordinates.x - 1, parent_node.coordinates.y - 1])
            next_node_value = matrix[parent_node.coordinates.x - 1][parent_node.coordinates.y - 1]
        elif direction == "U":
            next_node_coordinates = Point([parent_node.coordinates.x - 1, parent_node.coordinates.y])
            next_node_value = matrix[parent_node.coordinates.x - 1][parent_node.coordinates.y]
        # verify it's not a wall or out of bounds
        if next_node_coordinates.x < 0 or next_node_coordinates.y < 0 or next_node_value < 0:
            return Node()
        next_node_h_value = h_function(next_node_coordinates, end_point, min_value)
        list_of_cords = parent_node.list_of_cords[:]
        list_of_cords.append(parent_node.coordinates)
        return Node(coordinates=next_node_coordinates, cost=next_node_value,
                    path_to_node=parent_node.path_to_node + f'{direction}-', depth=parent_node.depth + 1,
                    g_cost_of_path=parent_node.g_cost_of_path + next_node_value,
                    heuristic_value=next_node_h_value,
                    f_cost_of_path=parent_node.g_cost_of_path + next_node_value + next_node_h_value,
                    list_of_cords=list_of_cords)
    except:
        return Node()


def get_children(node, matrix, h_function=zero_heuristic, end_point=Point([0, 0]), min_value = 1):
    children = []
    directions = ("RU", "R", "RD", "D", "LD", "L", "LU", "U")
    for direction in directions:
        current_node = get_node_in_direction(node, direction, matrix, h_function, end_point, min_value)
        if current_node.coordinates in node.list_of_cords:
            continue
        if current_node.cost > 0:
            children.append(current_node)
    return children
