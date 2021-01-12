# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dataStructures import DataInput, Point, StatsContainer
from inputChecks import check_input
import numpy
import Heuristics
from math import log2, sqrt
from Heuristics import euclidean_distance as h_func
import os.path
import xlwt
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

    elif input_data.selected_algorithm == "IDS":
        import IDS
        res = IDS.run(input_data, start_time, time_limit)

    elif input_data.selected_algorithm == "ASTAR":
        import UCS
        res = UCS.run(input_data, h_func, start_time, time_limit)

    elif input_data.selected_algorithm == "BIASTAR":
        import BI_Astar
        res = BI_Astar.run(input_data, h_func, start_time, time_limit)

    elif input_data.selected_algorithm == "IDASTAR":
        import IDAstar
        res = IDAstar.run(input_data, h_func, StatsContainer(), start_time, time_limit)

    if res is None:
        print("Incorrect algorithm name")
        return
    return res


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


# TODO: Replace list of cords to ancestors or something intuitive after final merge, change penetration to d/N
if __name__ == '__main__':

    algorithms = ['UCS', 'ASTAR', 'IDS', 'IDASTAR']

    wb = xlwt.Workbook()
    for algorithm in algorithms:
        stats_sheet = wb.add_sheet(f'{algorithm}_stats')
        stats_sheet.write(0, 0, 'Problem')
        stats_sheet.write(0, 1, 'Heuristic Name')
        stats_sheet.write(0, 2, 'N')
        stats_sheet.write(0, 3, 'd/N')
        stats_sheet.write(0, 4, 'Success (Y/N)')
        stats_sheet.write(0, 5, 'Time (sec)')
        stats_sheet.write(0, 6, 'EBF')
        stats_sheet.write(0, 7, 'Average H value')
        stats_sheet.write(0, 8, 'Min Depth')
        stats_sheet.write(0, 9, 'Avg Depth')
        stats_sheet.write(0, 10, 'Max Depth')
        total_success = total_h = total_nodes = total_penetration = total_time = total_ebf = total_mindepth = total_maxdepth = total_avgdepth = 0

        path = os.path.dirname(__file__)
        for i in range(18):
            test_name = f"test_{i}.txt"
            data = parse_input_file(os.path.join(path, test_name))
            data.selected_algorithm = algorithm
            legal, result = check_input(data)

            if legal is False:
                if result is None:
                    # Start/end point coordinates are illegal
                    print("Invalid coordinates of start point or end point.")
                else:
                    # Start point == End point
                    print("Start Point == End Point")
                    print(result)
            else:
                current_row = i + 1
                if data.selected_algorithm == "IDASTAR":
                    continue
                result = run_algorithm(data, 0, 0)
                if result.successful:
                    result_file = f"{algorithm}_test_{i}_results.txt"
                    with open(result_file, "w") as file:
                        file.write(result.get_results())
                result.problem = test_name
                if data.selected_algorithm == "ASTAR" or data.selected_algorithm == "IDASTAR" or data.selected_algorithm == "BIASTAR":
                    result.h_function = "chebyshev"
                success = 'Y' if result.successful else 'N'
                if result.successful:
                    total_success += 1
                    total_h += result.avg_H
                    total_time += result.time
                    total_nodes += result.nodes_expanded
                    total_ebf += result.EBF
                    total_maxdepth += result.max_depth
                    total_avgdepth += result.avg_depth
                    total_mindepth += result.min_depth
                    total_penetration += result.penetration

                stats_sheet.write(current_row, 0, f'{result.problem}')
                stats_sheet.write(current_row, 1, f'{result.h_function}')
                stats_sheet.write(current_row, 2, f'{result.nodes_expanded}')
                stats_sheet.write(current_row, 3, f'{result.penetration}')
                stats_sheet.write(current_row, 4, f'{success}')
                stats_sheet.write(current_row, 5, f'{result.time}')
                stats_sheet.write(current_row, 6, f'{result.EBF}')
                stats_sheet.write(current_row, 7, f'{result.avg_H}')
                stats_sheet.write(current_row, 8, f'{result.min_depth}')
                stats_sheet.write(current_row, 9, f'{result.avg_depth}')
                stats_sheet.write(current_row, 10, f'{result.max_depth}')
        stats_sheet.write(22, 0, "Totals and Averages")
        stats_sheet.write(22, 1, "Total Success:")
        stats_sheet.write(22, 2, "Average N")
        stats_sheet.write(22, 3, "Average H")
        stats_sheet.write(22, 4, "Average Time")
        stats_sheet.write(22, 5, "Average d/N")
        stats_sheet.write(22, 6, "Average Min Depth")
        stats_sheet.write(22, 7, "Average average Depth")
        stats_sheet.write(22, 8, "Average Max Depth")
        stats_sheet.write(22, 9, "Average EBF")

        if total_success == 0:
            total_h = total_nodes = total_penetration = total_time = total_ebf = total_mindepth = total_maxdepth = total_avgdepth = 0
            total_success = 1

        stats_sheet.write(23, 1, total_success)
        stats_sheet.write(23, 2, total_nodes / total_success)
        stats_sheet.write(23, 3, total_h / total_success)
        stats_sheet.write(23, 4, total_time / total_success)
        stats_sheet.write(23, 5, total_penetration / total_success)
        stats_sheet.write(23, 6, total_mindepth / total_success)
        stats_sheet.write(23, 7, total_avgdepth / total_success)
        stats_sheet.write(23, 8, total_maxdepth / total_success)
        stats_sheet.write(23, 9, total_ebf / total_success)
        wb.save('statistics.xls')
