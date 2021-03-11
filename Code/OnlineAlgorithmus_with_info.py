# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:37:12 2020

@author: benel
"""
# Change this back to Testen to make it work
import SingleAgentPathPlanner_v8 as Solver
from Visualisation_v1 import visualize
from matplotlib import animation
import time
import math
import All_station_layouts as demos
from random import randint
import copy
import itertools
import operator
from update_info import update
import random as r


# From stackoverflow https://stackoverflow.com/questions/1518522/find-the-most-common-element-in-a-list
def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

def run(entry_times, walls_in_model, stops, matching, station_start, station_end, actual_waiting_times, expected_waiting_times, printing_info = True):
    vehicles = {}
    for i in range(len(entry_times)):
        vehicles[i] = {}
        vehicles[i]['path'] = [] # The path the vehicle drives
        vehicles[i]['entry time'] = entry_times[i] # when does the vehicle enter the station
        vehicles[i]['exit time'] = math.inf # when does the vehicle exit the station
        vehicles[i]['stop done'] = False # did all passengers leave/enter the vehicle
        vehicles[i]['phase'] = 0 #0 = not in station, 1 = way to stop, 2 = way to exit
        vehicles[i]['time to wait'] = expected_waiting_times[i] # How long we ecpect the vehicle to wait
        vehicles[i]['actual waiting'] = 0 # How long does our vehicle actually wait
        vehicles[i]['time to stop'] = 0 # How long it takes from the station start to the stop
        vehicles[i]['time to exit'] = 0 # How long it takes from the stop to the station exit
        vehicles[i]['stop'] = [] # Coordinate of our stop
        vehicles[i]['algorithm update'] = -1 #for debugging to see where something was the code does something
    
    timestep_running_times = []
    obstacles = [] # here we want to collect all vehicles in the station
    vehicles_in_station = True
    t = -1 # we want to start the while loop at 0
    
    ti = time.time()
    while vehicles_in_station == True:
        t += 1
        vehicles_in_station_list = []
        obstacles = []
        run_t = time.time()
        for i in vehicles.keys():
            if vehicles[i]['entry time'] < t:
                obstacles.append(vehicles[i]['path'])
                
            # find all vehicles that are in the station at time t
            if vehicles[i]['entry time'] <= t and vehicles[i]['exit time'] > t:
                vehicles_in_station_list.append(i)
                
            
            # calculate the path for a vehicle that enters the station in our timestep
            if t == vehicles[i]['entry time']:
                run_solver = Solver.solve(station_start, [], station_end, vehicles[i]['time to wait'], walls_in_model, obstacles, 31, t, stops, matching, is_with_information = True)
                vehicles[i]['path'] = run_solver[0]
                vehicles[i]['phase'] = 1
                vehicles[i]['time to stop'] = run_solver[1]
                vehicles[i]['time to exit'] = run_solver[2]
                vehicles[i]['exit time'] = t + vehicles[i]['time to stop'] + vehicles[i]['time to wait'] + vehicles[i]['time to exit']
                vehicles[i]['stop'] = run_solver[3]
                obstacles.append(run_solver[0])
                
                   
        something_changed = False
        # check if any vehicles can continue earlier or have to wait longer at the stop
        for i in vehicles_in_station_list:
            if vehicles[i]['phase'] == 1:
                
                # Update if the vehicle can continue (can be a signal from the passenger aswell)
                if t == vehicles[i]['entry time'] + vehicles[i]['time to stop'] + actual_waiting_times[i] - 1:
                    vehicles[i]['phase'] = 2
                    vehicles[i]['stop done'] = True
                    vehicles[i]['actual waiting'] = t - vehicles[i]['entry time'] - vehicles[i]['time to stop'] + 1 # we update the real waiting time of the vehicle (+1 because we start counting waiting time as soon as we are in the stop)
                    
                    # Vehicle faster than expected
                    if vehicles[i]['actual waiting'] != vehicles[i]['time to wait']:
                        something_changed = True
                        
                
                # The vehcile stops longer than expected
                if t >= vehicles[i]['entry time'] + vehicles[i]['time to stop'] + vehicles[i]['time to wait'] - 1 and vehicles[i]['stop done'] == False:
                    something_changed = True
    
        
        # If anything changes in the timestep we recalculate all paths for all vehicles in the station
        if something_changed:
            
            teilzeit = time.time()
            update_paths = update(vehicles_in_station_list, obstacles, vehicles, t, station_end, walls_in_model)
            run_time = time.time()-teilzeit
            if printing_info:
                print('Timestep: ' + str(t))
                print(run_time)
            timestep_running_times.append(run_time)
            
            
            # If we cannot find a path with the current priorities we shuffle the priorities randomly
            error_nr = 0
            while update_paths[2] == 'error':
                error_nr += 1
                if error_nr == 1:
                    print('Error in timestep ' + str(t))
                print('Permutating priority of vehicles...')
                r.shuffle(vehicles_in_station_list)
                print('Trying to replan routes...')
                update_paths = update(vehicles_in_station_list, obstacles, vehicles, t, station_end, walls_in_model)
                
                if error_nr == 40:
                    raise ValueError('No paths could be found in timestep: ' + str(t))
                
            vehicles = copy.deepcopy(update_paths[0])
            obstacles = update_paths[1][:]
        
        
        
#    # Check if we have any planned crashings in any timestep
#        for tim in range(len(max(obstacles,key=len))):
#            timelist = []
#            for i in range(len(obstacles)):
#                if len(obstacles[i]) > tim:
#                    timelist.append(obstacles[i][tim])
#                else:
#                    timelist.append([math.inf, math.inf])
#            timelist_help = [x for x in timelist if x != [math.inf, math.inf]]
#            if len(timelist_help) == 0:
#                timelist_help.append(-1)
#            var = most_common(timelist_help)
#            how_often = timelist.count(var)
#            
#            if how_often > 1 and var != [math.inf, math.inf]:
#                print('Timestep: ' + str(t))
#                print('Time of crash: ' + str(tim))
#                print('Variable: ' + str(var))
#                print('How often : ' + str(how_often))
#                for j in range(len(timelist)):
#                    if timelist[j] == var:
#                        print('Vehicle: ' + str(j))
#                        print('Algorithm part: ' + str(vehicles[j]['algorithm update']))
#                print('\n')  
#
        # Update boolean
        if len(vehicles_in_station_list) < 1:
            vehicles_in_station = False
#            
#        run_time = time.time()-run_t
#        if printing_info:
#            print('Timestep: ' + str(t))
#            print(run_time)
#        timestep_running_times.append(run_time)
#    dauer = time.time() - ti
#    print(dauer)
    
  #################### This is just to confirm that everything works fine. We can delete that if we want to. ################################################
  #                                                                                                                                                         #
  #                                                                                                                                                         #    
#    
#    # Check if we have any crashings in our end configuration
    print('\n')    
    print('Start crashes')

    for t in range(len(max(obstacles,key=len))):
        timelist = []
        for i in range(len(obstacles)):
            if len(obstacles[i]) > t:
                timelist.append(obstacles[i][t])
            else:
                timelist.append([math.inf, math.inf])
        timelist_help = [x for x in timelist if x != [math.inf, math.inf]]     
        var = most_common(timelist_help)
        how_often = timelist.count(var)
        
        if how_often > 1 and var != [math.inf, math.inf]:
            print('Timestep: ' + str(t))
            print('Variable: ' + str(var))
            print('How often : ' + str(how_often))
            for j in range(len(timelist)):
                if timelist[j] == var:
                    print('Vehicle: ' + str(j))
            print('\n')  
    
    print('End crashes')
    
    # Check if all vehicles stop long enough
    for i in range(len(obstacles)):
        time_in_stop_real = obstacles[i].count(vehicles[i]['stop'])
    
        if time_in_stop_real < actual_waiting_times[i]:
            print('Not waited long enough: ' + str(i))
        
    #                                                                                                                                                       #
    #                                                                                                                                                       #
    #########################################################################################################################################################

        
    # This visualizes our solution and returns our KPIs.
    
    # We need a placeholder for the timesteps in which a vehicle isn't in the station
    # We clean that up here then for our visualization
    def clear_path(path):
            return[position for position in path if position != [math.inf,math.inf]]
    
    makespan = 0
    total_time = 0
    total_time_to_stop = 0
    total_time_to_exit = 0
    
    #Calculating parameters
    for i in range(len(obstacles)):
        obstacles[i] = clear_path(obstacles[i])
        obstacles[i].insert(0,entry_times[i])
        
        #print(obstacles[i])
        
        if obstacles[i][0] + len(obstacles[i]) - 1 > makespan:
            makespan = obstacles[i][0] + len(obstacles[i]) - 1
        
        total_time_to_stop += vehicles[i]['time to stop']
        total_time_to_exit += vehicles[i]['time to exit']
        total_time += vehicles[i]['time to stop'] + vehicles[i]['time to exit'] + vehicles[i]['actual waiting']
    
    stau = []
    
    for i in range(len(entry_times)):
        stau.append([[k,len(list(v))] for k,v in itertools.groupby(obstacles[i][1:])])
    
    
    stau_total = 0
    for i in range(len(stau)):
    
        for j in range(len(stau[i])):
            if stau[i][j][1] != 1:
                
                if stau[i][j][0] != vehicles[i]['stop']:
                    stau_total += stau[i][j][1] - 1
                if stau[i][j][0] == vehicles[i]['stop'] and stau[i][j][1] > vehicles[i]['actual waiting']:
                    stau_total += stau[i][j][1] - vehicles[i]['actual waiting']
    
    # Here we print all relevant numbers
#    print('Running time: ' + str(dauer))
#    print('\n')
#    print('Total time from entrance to stops: ' + str(total_time_to_stop))
#    print('Total time from stops to station exit: ' + str(total_time_to_exit))
#    print('Makespan: ' + str(makespan))
#    print('\n')
#    print('Average time from station entrance to stop: ' + str(total_time_to_stop/len(goals)))
#    print('Average time from stop to station exit: ' + str(total_time_to_exit/len(goals)))
#    print('Average total time per vehicle without waiting time: ' + str((total_time_to_stop + total_time_to_exit)/len(goals)))
#    print('Vehicles per 10 time units: ' + str(len(goals)/makespan*10))
#    print('Traffic indictor: ' + str(stau_total))
    
    return obstacles, vehicles, makespan, total_time, stau_total, timestep_running_times


# This one gives us our visualization
#walls_in_model.remove([3,19])
#outer_ani = visualize(obstacles, walls_in_model, [station_end[0], stops[0][1]])

#Uncomment when you want to save the animation
#writergif = animation.FFMpegWriter(fps=60) 
#outer_ani.save('name.mp4', writer=writergif)

