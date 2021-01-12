# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dataStructures import DataInput, Point, StatsContainer
from inputChecks import check_input
import numpy
import Heuristics
from math import log2, sqrt
from Heuristics import euclidean_distance as h_func
import os.path
import time
from sys import maxsize


def parse_input_file(file_path: str) -> DataInput:
    with open(file_path, 'r') as file:
        selected_algorithm = file.readline().rstrip('\n')
        matrix_size = int(file.readline())
        start_point = Point([int(num) for num in file.readline().split(',')])
        end_point = Point([int(num) for num in file.readline().split(',')])
        matrix = numpy.array([[float(num) for num in line.split(',')] for line in file.readlines()])
        min_value = maxsize
        for row in matrix:
            row_list = [i for i in row if i > 0]
            if len(row_list) > 0:
                row_min = min([i for i in row if i > 0])
                min_value = min(min_value, row_min)
        return DataInput(selected_algorithm, matrix_size, start_point, end_point, matrix, min_value)


def run_algorithm(input_data, time_limit, start_time=0.0):
    res = None
    if input_data.selected_algorithm == "UCS":
        import UCS
        res = UCS.run(input_data, Heuristics.zero_heuristic, start_time, time_limit)
        print(res)
    elif input_data.selected_algorithm == "IDS":
        import IDS
        res = IDS.run(input_data, start_time, time_limit)
        print(res)
    elif input_data.selected_algorithm == "ASTAR":
        import UCS
        res = UCS.run(input_data, h_func, start_time, time_limit)
        print(res)
    elif input_data.selected_algorithm == "BIASTAR":
        import BI_Astar
        res = BI_Astar.run(input_data, h_func, start_time, time_limit)
        print(res)
    elif input_data.selected_algorithm == "IDASTAR":
        import IDAstar
        res = IDAstar.run(input_data, h_func, StatsContainer(), start_time, time_limit)
        print(res)
    if res is None:
        print("Incorrect algorithm name")
        return
    file_name = f'{input_data.selected_algorithm}_latest_test_results.txt'
    with open(file_name, "w") as result_file:
        result_file.write(res.__str__())


# TODO: Replace list of cords to ancestors or something intuitive after final merge, change penetration to d/N
def get_suggested_time_limit(data):
    algo = data.selected_algorithm
    if algo == "ASTAR" or algo == "UCS" or algo == "BIASTAR":
        res = log2(data.matrix_size)
    elif algo == "IDS":
        res = sqrt(data.matrix_size)
    else:
        res = data.matrix_size / 2
    return round(res, 2)


if __name__ == '__main__':

    # ___uncomment this when switching to I/O___ #
    data = parse_input_file(input("Drag your file here:\n"))
    suggested_limit = get_suggested_time_limit(data)
    user_wants_to_set_new_time = input(
        f'Suggested time limit for this file is: {suggested_limit}, would you like to enter a different time limit? (Y/N)\n')
    user_wants_to_set_new_time.upper()
    if user_wants_to_set_new_time == 'Y':
        runtime_limit = input("Please enter a new time limit: \n")
    else:
        runtime_limit = suggested_limit

    # _____for testing____ #
    # path = os.path.dirname(__file__)
    # test_name = "medium_test.txt"
    # data = parse_input_file(os.path.join(path, test_name))
    # runtime_limit = 0

    start_time = time.process_time()
    legal, result = check_input(data)
    if legal is False:
        if result is None:
            # Start/end point coordinates are illegal
            print("Error: Invalid coordinates of start point or end point.")
        else:
            if legal is True:
                # Start point == End point
                print("Start Point == End Point!\n")
                print(result)
            else:
                # Root Cost is -1
                print("Error: Root Cost is -1")
    else:
        run_algorithm(data, runtime_limit, start_time)
