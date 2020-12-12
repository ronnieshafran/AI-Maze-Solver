# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dataStructures import DataInput, Point
import numpy


def parseInputFile(filePath: str) -> DataInput:
    with open(filePath, 'r') as file:
        selected_algorithm = file.readline().rstrip('\n')
        matrixSize = int(file.readline())
        start_point = Point([int(num) for num in file.readline().split(',')])
        end_point = Point([int(num) for num in file.readline().split(',')])
        matrix = numpy.array([[int(num) for num in line.split(',')] for line in file.readlines()])
        return DataInput(selected_algorithm, matrixSize, start_point, end_point, matrix)


if __name__ == '__main__':
    di = parseInputFile(r'C:\Users\ronni\PycharmProjects\AIFinalProject\t.txt')
    if di.selected_algorithm == "UCS":
        import UCS
        res = UCS.run(di)
        print(res)
    else:
        raise Exception("something crashed :(")
