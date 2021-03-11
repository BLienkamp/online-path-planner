# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 13:27:19 2021

@author: benel
"""


from Visualisation_v1 import visualize
from matplotlib import animation
import All_station_layouts as demos
import OnlineAlgorithmus_with_info as OA
import time
import Scenarios



def runOA_with_info(stop_assignment = 'ordered front to back', demo_index = "1_9stops",scenario_index = '_base', perfect_estimation = False, show_timesteps = True):
    ################ Here you can specify which instance to run with which parameters ###############
    #                                                                                               #    
    #                                                                                               # 
    
    # stop_assignment = 'ordered front to back'
    # demo_index = "1_4stops"
    # scenario_index = '_base'
    # # Are the estimated waiting times equal to the actual waiting times
    # perfect_estimation = True 
    
    #                                                                                               #    
    #                                                                                               #    
    #################################################################################################
    
    
    ######################## Here everything gets set up to run the scenario ########################
    #                                                                                               #    
    #                                                                                               #   
    
    print('Station layout: ' + str(demo_index))
    print('Stop assignment: ' + str(stop_assignment))
    print('Scenario: ' + str(scenario_index))
    walls_in_model = []
    stops = []
    walls_in_model = getattr(demos, 'walls'+str(demo_index))[:]
    stops = getattr(demos, 'stops'+str(demo_index))[:]
    station_start = getattr(demos, 'station_start'+str(demo_index))
    station_end = getattr(demos, 'station_end'+str(demo_index))
    
    scenario = getattr(Scenarios, 'scenario'+str(scenario_index))
    
    # This is only used as some form of signal
    entry_times = scenario['entry_times']
    actual_waiting_times = scenario['actual_waiting_times']
    
    # Change this if you want to test expected_waiting_times == actual_waiting_times
    if perfect_estimation:
        expected_waiting_times = actual_waiting_times
    else:
        expected_waiting_times = scenario['expected_waiting_times']
    
        
    #                                                                                               #    
    #                                                                                               #    
    #################################################################################################
    
    
    
    ######################## This runs our algorithm, in this case no info ##########################
    #                                                                                               #    
    #                                                                                               # 
    
    t = time.time()
    run = OA.run(entry_times, walls_in_model, stops, stop_assignment, station_start, station_end, actual_waiting_times, expected_waiting_times, printing_info = show_timesteps)
    running_time = time.time() - t
    #                                                                                               #    
    #                                                                                               #    
    #################################################################################################
    
    
    
    ################################ Here we visualize the solution #################################
    #                                                                                               #    
    #                                                                                               # 
    
    obstacles = run[0]
    vehicles = run[1]
    makespan = run[2]
    total_time = run[3]
    traffic_indicator = run[4]
    timestep_running_times = run[5] 

    print('\n')
    print('Running time: ' + str(running_time))
    if len(timestep_running_times) > 0:
        print('Max timestep running time: ' + str(max(timestep_running_times)))
    print('Total time: ' + str(total_time))
    print('Makespan: ' + str(makespan))
    print('Traffic indictor: ' + str(traffic_indicator))
    # walls_in_model.remove([3,19])
    # outer_ani = visualize(obstacles, walls_in_model, [station_end[0], stops[0][1]])
    
    #                                                                                               #    
    #                                                                                               #    
    #################################################################################################
    
    return obstacles, total_time, makespan, traffic_indicator, running_time, (walls_in_model, station_end, stops)


# Uncomment to run specific scenarios
# RUN = runOA_with_info(demo_index='1_9stops', scenario_index = '1_rush')
# outer_ani = visualize(RUN[0], RUN[5][0], [RUN[5][1][0], RUN[5][2][0][1]])