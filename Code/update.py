# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 10:21:30 2020

@author: benel
"""
import SingleAgentPathPlanner_v6 as Solver
import math

def update(vehicles_in_station_list, obstacles, vehicles, t, station_end, walls_in_model):

    # delete all paths of the vehicles in the station
    for i in vehicles_in_station_list:
        obstacles[i] = []
        
        current_position = []
        for j in range(t):
            current_position.append([math.inf, math.inf])
        
        current_position.append(vehicles[i]['path'][t])
        obstacles[i] = current_position

    # Recalculate all paths
    for i in vehicles_in_station_list:
        obstacles[i] = []
        # vehicle is stopping but not done
        if vehicles[i]['stop done'] == False and vehicles[i]['path'][t] == vehicles[i]['stop'] and t>= vehicles[i]['entry time'] + vehicles[i]['time to stop']:

            # We stay one more timestep in the stop
            vehicles[i]['path'].append(vehicles[i]['stop'])

            
            obstacles[i] = vehicles[i]['path']
            vehicles[i]['algorithm update'] = 1
        
        # faster vehicle or vehicle already in phase 2
        elif vehicles[i]['stop done'] == True and vehicles[i]['phase'] == 2:
                    
            # if the vehicle is in the exit node we don't recalculate
            if vehicles[i]['path'][t] == station_end:
                continue
            
            vehicles[i]['algorithm update'] = 2
            
            try:
                update = Solver.update(vehicles[i]['path'][t], [], station_end, 0, walls_in_model, obstacles, 31, t,  vehicles[i]['phase'])
            
            except ValueError:
                return ({},[], 'error')
            else:
                vehicles[i]['time to exit'] = t - (vehicles[i]['entry time'] + vehicles[i]['time to stop'] + vehicles[i]['actual waiting']) + update[1]
                vehicles[i]['exit time'] = vehicles[i]['entry time'] + vehicles[i]['time to stop'] + vehicles[i]['time to exit'] + vehicles[i]['actual waiting']
                new_path = vehicles[i]['path'][:t] + update[0]
                         
            # Get new path
            vehicles[i]['path'] = new_path[:]
            obstacles[i] = vehicles[i]['path'][:]
            
            
        
        # recalculate vehicles that are still on their way to the stop
        elif vehicles[i]['stop done'] == False and vehicles[i]['phase'] == 1:
                
                
            if vehicles[i]['path'][t] != vehicles[i]['stop']:
                vehicles[i]['algorithm update'] = 5
                
                try:
                    update = Solver.update(vehicles[i]['path'][t], vehicles[i]['stop'], station_end, 0, walls_in_model, obstacles, 31, t, 1)
                    #update = Solver.update(vehicles[i]['path'][t], vehicles[i]['stop'], station_end, vehicles[i]['time to wait'], walls_in_model, obstacles, 31, t, 1)
                
                except ValueError:
                    return ({},[], 'error')
                
                else:
                # Get new path
                    new_path = vehicles[i]['path'][:t] + update[0][t:]
                    vehicles[i]['path'] = new_path[:]
                    obstacles[i] = new_path[:]
                    
                    vehicles[i]['time to stop'] = update[1] + (t - vehicles[i]['entry time'])
        
        # did we forget anything
        else:
            vehicles[i]['algorithm update'] = 0
            
    return (vehicles, obstacles, 'no error')