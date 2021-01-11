# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dataStructures import DataInput, Point, StatsContainer
from inputChecks import check_input
import numpy
import Heuristics
import os.path
import xlwt


def parse_input_file(file_path: str) -> DataInput:
    with open(file_path, 'r') as file:
        selected_algorithm = file.readline().rstrip('\n')
        matrix_size = int(file.readline())
        start_point = Point([int(num) for num in file.readline().split(',')])
        end_point = Point([int(num) for num in file.readline().split(',')])
        matrix = numpy.array([[float(num) for num in line.split(',')] for line in file.readlines()])
        return DataInput(selected_algorithm, matrix_size, start_point, end_point, matrix)


def run_algorithm(input_data):
    res = None
    if input_data.selected_algorithm == "UCS":
        import UCS
        res = UCS.run(input_data, Heuristics.zero_heuristic)
        # print(res)
    elif input_data.selected_algorithm == "IDS":
        import IDS
        res = IDS.run(input_data)
        # print(res)
    elif input_data.selected_algorithm == "ASTAR":
        import UCS
        res = UCS.run(input_data, Heuristics.octile_distance)
        # print(res)
    elif input_data.selected_algorithm == "BIASTAR":
        import BI_Astar
        res = BI_Astar.run(input_data, Heuristics.octile_distance)
        # print(res)
    elif input_data.selected_algorithm == "IDASTAR":
        import IDAstar
        res = IDAstar.run(input_data, Heuristics.octile_distance, StatsContainer())
        # print(res)
    else:
        raise Exception("something went wrong :(")
    return res


# TODO: Replace list of cords to ancestors or something intuitive after final merge, change penetration to d/N
if __name__ == '__main__':

    algorithms = ['UCS','ASTAR','IDS','IDASTAR','BIASTAR']

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

        path = os.path.dirname(__file__)
        for i in range(20):
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
                current_row = i+1
                if data.selected_algorithm == "IDASTAR":
                    continue
                result = run_algorithm(data)
                if result.successful:
                    result_file = f"{algorithm}_test_{i}_results.txt"
                    with open(result_file, "w") as file:
                        file.write(result.get_results())
                result.problem = test_name
                if data.selected_algorithm == "ASTAR" or data.selected_algorithm == "BIASTAR" or data.selected_algorithm == "BIASTAR":
                    result.h_function="chebyshev"
                success = 'Y' if result.successful else 'N'
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
        wb.save('statistics.xls')

