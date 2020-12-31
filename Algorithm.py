import dataStructures
import Heuristics


def run(di):
    if di.selected_algorithm == "IDS":
        return IDS(di)
    elif di.selected_algorithm == "UCS":
        return UCS(di, Heuristics.zero_heuristic)
    elif di.selected_algorithm == "ASTAR":
        return Astar(di, Heuristics.euclidean_distance)
    elif di.selected_algorithm == "IDASTAR":
        return IDAstar(di, Heuristics.euclidean_distance)
    elif di.selected_algorithm == "BIASTAR":
        return BIAstar(di, Heuristics.euclidean_distance)
    else:
        return null
