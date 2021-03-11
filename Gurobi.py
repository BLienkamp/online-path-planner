# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 17:15:42 2020

@author: benel
"""

# THIS FILE CAN ONLY BE EXECUTED WITH A WORKING GUROBI LICENSE
import gurobipy as gp
from gurobipy import GRB
import All_station_layouts as demos
from Visualisation_v1 import visualize
import math
import Scenarios
import itertools
import time

def run_benchmark(demo_index = "1_9stops",scenario_index = '1_rush', obj = 'total time', max_run_time = 20*60, max_time = 80):
   
    
    ######################## Here everything gets set up to run the scenario ########################
    #                                                                                               #    
    #                                                                                               #   
    
    print('Station layout: ' + str(demo_index))
    print('Scenario: ' + str(scenario_index))
    # We need the walls only for the visualization in the end
    walls_in_model = []
    walls_in_model = getattr(demos, 'walls'+str(demo_index))[:]
    
    # Get all stops
    stops = []
    stops = getattr(demos, 'stops'+str(demo_index))[:]
    # We need to convert the lists into tuples
    for i in range(len(stops)):
        stops[i] = tuple(stops[i])
        
    # Get station start and end 
    station_start = tuple(getattr(demos, 'station_start'+str(demo_index)))
    station_end = tuple(getattr(demos, 'station_end'+str(demo_index)))
    
    # Get the scenario we want to run
    scenario = getattr(Scenarios, 'scenario'+str(scenario_index))
    
    # Get the real entry and waiting times
    entry_times = scenario['entry_times']
    actual_waiting_times = scenario['actual_waiting_times']
    
    # Add a list of vehicle indices
    vehicles = []
    for i in range(len(entry_times)):
        vehicles.append(i)
        
    # Get all possible positions of a station
    positions = getattr(demos, 'positions'+str(demo_index))[:]
    
    # A list of all timesteps we need
    times = []
    for t in range(max_time):
            times.append(t)
            
            
    times_until_station_entered = []
    possible_times_in_station = []
    for v in vehicles:
        times_until_station_entered.append([])
        possible_times_in_station.append([])
        for t in range(max_time):
            if entry_times[v] > t:
                times_until_station_entered[v].append(t)
            if entry_times[v] < t:
                possible_times_in_station[v].append(t)
        
    #                                                                                               #    
    #                                                                                               #    
    #################################################################################################
             
    # This function returns all possible neighbours of a position (including the position itself)
    def neighbours(position):
        possible_neighbours = []
        candidate = (0,0)
        for i in range(5):
            
            if i == 0:
                candidate = position
    
            if i == 1:
                candidate = (position[0]-1, position[1])
                
            if i == 2:
                candidate = (position[0]+1, position[1])
                
            if i == 3:
                candidate = (position[0], position[1]-1)
            
            if i == 4:
                candidate = (position[0], position[1]+1)
            possible_neighbours.append(candidate)
        
        neighbours = []
        for candidate in possible_neighbours:
            if candidate in positions:
                neighbours.append(candidate)
        
        return neighbours
    
    
    # This function finds the Benchmark solution
    def opti(positions, obj, time_limit):
        # Here we get all possible arcs in our station
        arcs_list = gp.tuplelist()
        for position in positions:
            neighbours_list = neighbours(position)
            for neighbour in neighbours_list:
                arcs_list.append((position,neighbour))
        m = gp.Model()
        
        
        
        # 1 if vehicle i uses an arcs at time t
        arcs = m.addVars(vehicles, arcs_list, times, vtype = GRB.BINARY, name = 'arcs')
    
        # No arc is used until the vehicle enters the station
        for v in vehicles:
            m.addConstr(gp.quicksum(arcs[v,i, j, t] for i,j in arcs_list for t in times_until_station_entered[v]) == 0, name = 'pre_arrival_%s' %v)
        
        # When a vehicle enters the station it uses the first arc
        for v in vehicles:
            m.addConstr(arcs[v,(0,19),(1,19), entry_times[v]] == 1, name = 'arrival_%s' %v)
            
        # A vehicle can only use at most one arc every timestep
        for v in vehicles:
            for t in times:
               m.addConstr(gp.quicksum(arcs[v,i,j,t] for i,j in arcs_list) <= 1, name = 'one arc at a time')
            
        # An arc can only be used by one vehicle in the same direction
        for t in times:  
            for i,j in arcs_list:
                m.addConstr(gp.quicksum(arcs[v, i, j, t] for v in vehicles) <= 1, name = 'only one vehicle per arc one direction')
        
        # An arc can only be used by one vehicle in opposite directions
        for t in times:
            for i,j in arcs_list:
                if i != j:
                    m.addConstr((1-gp.quicksum(arcs[v, i, j, t] for v in vehicles)) >= gp.quicksum(arcs[v, j, i, t] for v in vehicles), name = 'only one vehicle per arc opposite direction')
        
        # Only one vehicle can drive to one node in every timestep
        for t in times:
            for position in positions:
                m.addConstr(gp.quicksum(arcs[v, i, position, t] for v in vehicles for i in neighbours(position)) <= 1, name = 'only one vehicle in every node')
                
        # Flow conservation for every vehicle in every node
        for t in times[:-1]:
            for position in positions:
                if position != station_start and position != station_end:
                    for v in vehicles:
                        if t < entry_times[v]:
                            continue
                        m.addConstr(gp.quicksum(arcs[v, i, position, t] for i in neighbours(position)) == gp.quicksum(arcs[v, position, j, t+1] for j in neighbours(position)), 
                                    name = 'flow 1 position %s at time %s' %(position, t))
    
        
        # Vehicle doesn't go back to station_start
        for v in vehicles:
            m.addConstr(gp.quicksum(arcs[v, station_start, j, t] for j in neighbours(station_start) for t in times) == 1, name = 'station_start 1')
        for v in vehicles:
            m.addConstr(gp.quicksum(arcs[v, i, station_start, t] for i in neighbours(station_start) for t in times) == 0, name = 'station_start 2')
            
        # Vehicle doesn't go back into the station from station_end
        for v in vehicles:
            m.addConstr(gp.quicksum(arcs[v, i, station_end, t] for i in neighbours(station_end) for t in times) == 1, name = 'station_end 1')
        for v in vehicles:
            m.addConstr(gp.quicksum(arcs[v, station_end, j, t] for j in neighbours(station_end) for t in times) == 0, name = 'station_end 2')
       
        
        #### Every vehicle has to drive to a stop and wait the given waiting time (goal[v][0]) ####
        
        # New variable that checks if the waiting procedure starts at timestep t in 'stop'
        waiting_variables = m.addVars(vehicles, stops, times, vtype = GRB.BINARY, name = 'waiting')
        
        # All waiting time starts that are not possible get assigned 0
        for v in vehicles:
            for t in times:
                for stop in stops:
                    if t+actual_waiting_times[v]+ math.fabs(stop[0] - station_end[0]) + math.fabs(stop[1] - station_end[1]) > max_time or t + 1 < math.fabs(stop[0] - station_start[0]) + math.fabs(stop[1] - station_start[1]):
                        m.addConstr(waiting_variables[v, stop[0], stop[1], t] == 0, name = 'impossible waiting starts')
        # This waiting variable is only 1 if the vehicle is in the stop for the needed waiting time
        for v in vehicles:
            for t in times:
                must_wait = []
                for wait in range(1,actual_waiting_times[v]):
                    if t+wait < max_time:
                        must_wait.append(t+wait)
                
                for stop in stops:
                    m.addConstr(actual_waiting_times[v]*waiting_variables[v, stop[0], stop[1], t] <=  gp.quicksum(arcs[v, i, stop, t] for i in neighbours(stop)) + gp.quicksum(arcs[v, stop, stop, wait] for wait in must_wait), name = 'waiting variable constr')
        # Every vehicle has to do the stop
        for v in vehicles:
            m.addConstr(gp.quicksum(waiting_variables[v, stop[0], stop[1], t] for stop in stops for t in times) == 1, name = 'stop done')
        
        
        
        
        
        # Set the objective
        if obj == 'total time':
            objective = gp.quicksum(arcs[v,i,j,t] for i,j in arcs_list for t in times for v in vehicles)
        
        if obj == 'makespan':
            # New variable makespan which is 1 in the timestep "time" in which the last vehicle left the station and 0 otherwise
            makespan = m.addVars(times, vtype = GRB.BINARY, name = 'makespan')
            
            # Can only be 1 if all vehicles left the station
            for time in times:
                m.addConstr(gp.quicksum(arcs[v, i, station_end, t] for v in vehicles for i in neighbours(station_end) for t in range(time)) >= len(vehicles)*makespan[time])
                
            # Only one variable is one the others 0
            m.addConstr(gp.quicksum(makespan[time] for time in times) == 1)
            
            # Fid the smallest timestep in which all vehicles left the station == makespan
            objective = gp.quicksum(time*makespan[time] for time in times)
    
        m.setObjective(objective, GRB.MINIMIZE)
        
        #Timelimit for the solver
        m.setParam('TimeLimit', time_limit)
        #m.setParam('Symmetry', 2)
        m.optimize()
    
        # Uncomment this if the model is not solvable to find out which constraints lead to that
        # m.computeIIS()
        
        # for c in m.getConstrs():
        #     if c.IISConstr:
        #         print('%s' % c.constrName)
        
        
    #     Get a path out of that solution
        path = []
        for v in vehicles:
            path.append([entry_times[v], station_start])
        
        # Do we still need that?
        #TODO
    #    solution = m.getVars()
    #
    #    
    #    for v in solution:
    #        if v.X ==1:
    #            print("{}: {}".format(v.varName, v.X))
    #        
        for v in vehicles:
            for t in times:
                for i,j in arcs_list:
                    if m.getVarByName('arcs[%s,%s,%s,%s]' %(v,i,j,t)).X == 1:
                        path[v].append([j[0], j[1]])
         
        stops_of_vehicles = []               
        for v in vehicles:
            for t in times:
                for stop in stops:
                    if m.getVarByName('waiting[%s,%s,%s,%s]' %(v,stop[0],stop[1],t)).X == 1:
                        stops_of_vehicles.append([stop[0],stop[1]])
                        
        return m,path, m.objval, stops_of_vehicles
    
    
    # This calculates the makespan of the paths we give it
    def calculate_makespan(paths):
        makespan = 0
        
        # We need -2 because we start in 0
        for path in paths:
            if path[0] + len(path)-2 > makespan:
                makespan = path[0] + len(path)-2
                
        return makespan
    
    # This calculates the total time of the path we give it
    def calculate_total_time(paths):
        total_time = 0
        
        for path in paths:
            total_time += len(path) - 2
        
            
        return total_time
    
    ########################### This runs the optimization and prints some parameters comment out of not needed ##############################
    #                                                                                                                                        #
    #                                                                                                                                        #
    
    t = time.time()
    optimize = opti(positions, obj, max_run_time)
    running_time = time.time() - t
    paths = optimize[1]
    model = optimize[0]
    objval = optimize[2]
    stops_of_vehicles = optimize[3]
    
    # Here we calculate the traffic
    stau = []
    
    for i in range(len(entry_times)):
        stau.append([[k,len(list(v))] for k,v in itertools.groupby(paths[i][1:])])
    
    
    stau_total = 0
    for i in range(len(stau)):
    
        for j in range(len(stau[i])):
            if stau[i][j][1] != 1:
                
                if stau[i][j][0] != stops_of_vehicles[i]:
                    stau_total += stau[i][j][1] - 1
                if stau[i][j][0] == stops_of_vehicles[i] and stau[i][j][1] > actual_waiting_times[i]:
                    stau_total += stau[i][j][1] - actual_waiting_times[i]
                    
    if obj == 'total time':
        print('Total time: ' + str(objval))
        makespan = calculate_makespan(paths)
        print('Makespan : ' + str(makespan))
        total_time = objval
    
    if obj == 'makespan':
        makespan = objval
        print('Makespan: ' + str(objval))     
        total_time = calculate_total_time(paths)
        print('Total time: ' + str(total_time))
    print('Traffic indicator: ' + str(stau_total))
    
    #                                                                                                                                        #
    #                                                                                                                                        #
    ##########################################################################################################################################
    return paths, total_time, makespan, stau_total, running_time, (walls_in_model, station_end, stops)





############################# Run a specific scenario. Comment out if not needed. ########################################################
#                                                                                                                                        #
# layout = '1_9stops'
# scenario = '1_rush'


# run_benchmark = run_benchmark(layout, scenario, 'total time', max_run_time=20*60, max_time=65)

# outer_ani = visualize(run_benchmark[0], run_benchmark[5][0], run_benchmark[5][1])

#                                                                                                                                        #
##########################################################################################################################################
