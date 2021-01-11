# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dataStructures import DataInput, Point, StatsContainer
from inputChecks import check_input
import numpy
import Heuristics
import os.path
import time


def parse_input_file(file_path: str) -> DataInput:
    with open(file_path, 'r') as file:
        selected_algorithm = file.readline().rstrip('\n')
        matrix_size = int(file.readline())
        start_point = Point([int(num) for num in file.readline().split(',')])
        end_point = Point([int(num) for num in file.readline().split(',')])
        matrix = numpy.array([[float(num) for num in line.split(',')] for line in file.readlines()])
        return DataInput(selected_algorithm, matrix_size, start_point, end_point, matrix)


def run_algorithm(input_data, time_limit):
    if input_data.selected_algorithm == "UCS":
        import UCS
        res = UCS.run(input_data, Heuristics.zero_heuristic, time_limit)
        print(res)
    elif input_data.selected_algorithm == "IDS":
        import IDS
        res = IDS.run(input_data, time_limit)
        print(res)
    elif input_data.selected_algorithm == "ASTAR":
        import UCS
        res = UCS.run(input_data, Heuristics.octile_distance, time_limit)
        print(res)
    elif input_data.selected_algorithm == "BIASTAR":
        import BI_Astar
        res = BI_Astar.run(input_data, Heuristics.octile_distance, time_limit)
        print(res)
    elif input_data.selected_algorithm == "IDASTAR":
        import IDAstar
        print(IDAstar.run(input_data, Heuristics.octile_distance, StatsContainer()), time_limit)
    else:
        raise Exception("something went wrong :(")


# TODO: Replace list of cords to ancestors or something intuitive after final merge, change penetration to d/N
if __name__ == '__main__':
    runtime_limit = input("Please enter time limit for the program\n")
    path = os.path.dirname(__file__)
    test_name = "medium_test.txt"
    data = parse_input_file(os.path.join(path, test_name))
    legal, result = check_input(data)

    if legal is False:
        if result is None:
            # Start/end point coordinates are illegal
            print("Invalid coordinates of start point or end point.")
        else:
            if legal is True:
                # Start point == End point
                print("Start Point == End Point")
                print(result)
            else:
                # Root Cost is -1
                print("Root Cost is -1")
                print(result)
    else:
        run_algorithm(data, runtime_limit)
