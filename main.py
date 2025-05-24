import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt

try:
    mpl.use('Qt5Agg')
except ImportError:
    mpl.use('TkAgg')

from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.visualization.mp_renderer import MPRenderer

# add current directory to python path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from SMP.maneuver_automaton.maneuver_automaton import ManeuverAutomaton
from SMP.motion_planner.motion_planner import MotionPlanner
from SMP.motion_planner.plot_config import StudentScriptPlotConfig


def main():
    # configurations
    path_scenarios = ['Scenarios/scenario1.xml', 'Scenarios/scenario2.xml', 'Scenarios/scenario3.xml']
    file_motion_primitives = 'V_9.0_9.0_Vstep_0_SA_-0.2_0.2_SAstep_0.4_T_0.5_Model_BMW320i.xml'
    config_plot = StudentScriptPlotConfig(DO_PLOT=True)

    for path_scenario in path_scenarios:
        # load scenario and planning problem set
        scenario, planning_problem_set = CommonRoadFileReader(path_scenario).open()
        # retrieve the first planning problem
        planning_problem = list(planning_problem_set.planning_problem_dict.values())[0]

        # create maneuver automaton and planning problem
        automaton = ManeuverAutomaton.generate_automaton(file_motion_primitives)

        # comment out the planners which you don't want to execute
        dict_motion_planners = {
            #0: (MotionPlanner.DepthFirstSearch, "Depth First Search"),
            1: (MotionPlanner.Astar, "A* Search"),
            #2: (MotionPlanner.IterativeDeepeningAstar, "Iterative Deepening A* Search")
        }
        for (class_planner, name_planner) in dict_motion_planners.values():
            planner = class_planner(scenario=scenario, planning_problem=planning_problem,
                                    automaton=automaton, plot_config=config_plot)
            # start search for various weight
            print("=================================================")
            #weight_list = [10, 1, 3, 5, 10]
            weight_list = [10]
            i = 0
            for w in weight_list:
                print(name_planner, '(w=', end='')
                print(weight_list[i], end='')
                print(')')
                """Execute Weighted A star search"""
                planner.w = weight_list[i]
                found = planner.execute_search(time_pause=0.01)
                print("\tVisited Nodes number:", len(planner.visited_nodes))
                print("\tPath: ", end='')
                planner.print_path()
                #print("\tHeuristic Cost (initial node):", planner.advanced_heuristic_function(planner.node_initial))
                print("\tHeuristic Cost (initial node):", planner.euclidean_heuristic_function(planner.node_initial))
                print("\tEstimated Cost:", planner.goal_node_reached.cost)
                i += 1
    print('Done')

if __name__ == '__main__':
    main()
