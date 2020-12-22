# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dataStructures import DataInput, Point
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

    dir_path = os.path.dirname(__file__)
    test_name = "large_test.txt"
    test_path = os.path.join(dir_path, test_name)
    di = parse_input_file(test_path)

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
    else:
        raise Exception("something went wrong :(")
