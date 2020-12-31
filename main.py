# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dataStructures import DataInput, Point, StatsContainer
import numpy
import Heuristics
import os.path


def parse_input_file(file_path: str) -> DataInput:
    with open(file_path, 'r') as file:
        selected_algorithm = file.readline().rstrip('\n')
        matrix_size = int(file.readline())
        start_point = Point([int(num) for num in file.readline().split(',')])
        end_point = Point([int(num) for num in file.readline().split(',')])
        matrix = numpy.array([[int(num) for num in line.split(',')] for line in file.readlines()])
        return DataInput(selected_algorithm, matrix_size, start_point, end_point, matrix)


# TODO: general TODOs: calc run time, refactor data structures to different files (?), find better name for UCS/A*
#  common function
if __name__ == '__main__':

    path = os.path.dirname(__file__)
    test_name = "large_test.txt"
    di = parse_input_file(os.path.join(path, test_name))

    if di.selected_algorithm == "UCS":
        import UCS
        res = UCS.run(di, Heuristics.zero_heuristic)
        print(res)
    elif di.selected_algorithm == "IDS":
        import IDS

        res = IDS.run(di)
        print(res)
    elif di.selected_algorithm == "ASTAR":
        import UCS

        res = UCS.run(di, Heuristics.euclidean_distance)
        print(res)

    elif di.selected_algorithm == "IDA*":
        import IDAstar
        print(ida_star(di, Heuristics.euclidean_distance, StatsContainer()))

    else:
        raise Exception("something went wrong :(")
