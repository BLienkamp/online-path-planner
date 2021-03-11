# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 09:44:16 2020

@author: benel
"""
import math
import random



######################################## Setup with which we can generate the search tree for A* ########################################
class Configuration(object):                                                                                                            #
                                                                                                                                        #
    def __init__(self, cfg, list_of_dynamic_obstacles):
        self.cfg = cfg
        self.obstacles = list_of_dynamic_obstacles
        self.safe_intervals = self.safe_intervals()
        
    def safe_intervals(self):
        times_obstacles_in_cfg = []
        
        
        # here we have to calculate the safe intervals for our dummy node since we have to make sure that 
        # no agents goes through the stop when we are standing there
        if self.cfg == [-1,-1]:
            
            # Here we collect all the timesteps in which an obstacle passes our configuration ((x,y)-coordinate)
            for obstacle_number in range(len(self.obstacles)):
                for i in range(len(self.obstacles[obstacle_number])):
                    if self.obstacles[obstacle_number][i] == first_goal and i not in times_obstacles_in_cfg:
                        times_obstacles_in_cfg.append(i)
                    
                    
            # If no obstacles pass our configuration we return an empty list
            if len(times_obstacles_in_cfg) < 1:
                return [[0,math.inf]]
            
            intervals = []
            sorted_times = sorted(times_obstacles_in_cfg)
            
            if sorted_times[0] > waiting_time:
                intervals.append([0,sorted_times[0] - waiting_time])
                
            for i in range(len(sorted_times) - 1):
                if sorted_times[i+1] - sorted_times[i] > waiting_time + 1:
                    interval_start = sorted_times[i] + 1
                    interval_end = sorted_times[i+1] - waiting_time
                    intervals.append([interval_start, interval_end])
            intervals.append([sorted_times[-1] + 1, math.inf])
            
            return intervals
                
                
                
        else:       
            # Here we collect all the timesteps in which an obstacle passes our configuration ((x,y)-coordinate)
            for obstacle_number in range(len(self.obstacles)):
                for i in range(len(self.obstacles[obstacle_number])):
                    if self.obstacles[obstacle_number][i] == self.cfg and i not in times_obstacles_in_cfg:
                        times_obstacles_in_cfg.append(i)
            
            # If no obstacles pass our configuration we return an empty list
            if len(times_obstacles_in_cfg) < 1:
                return [[0,math.inf]]
            
            # Here we want to get the intervals
            intervals = []
            sorted_times = sorted(times_obstacles_in_cfg)
            
            # This is the first safe interval
            if sorted_times[0] > 0:
                intervals.append([0,sorted_times[0] - 1])
            
            interval_start = sorted_times[0] + 1
            interval_end = math.inf
            
            # If we find an interval we add it to the list of intervals
            for i in range(len(sorted_times) - 1):
                if sorted_times[i+1] - sorted_times[i] > 1:
                    interval_start = sorted_times[i] + 1
                    interval_end = sorted_times[i+1]-1
                    intervals.append([interval_start,interval_end])
            intervals.append([sorted_times[-1]+1,math.inf])
        

        
        return intervals

class SearchState(object):
    
    def __init__(self, Configuration, g = math.inf, f = math.inf, interval = 0, t = 0, parent = None):
        self.Configuration = Configuration
        self.cfg = Configuration.cfg
        self.safe_intervals = Configuration.safe_intervals
        self.g = g
        self.f = f
        self.interval = interval
        self.time = t
        # Right now this parent is a Search State again. So we save everything atleast twice which isn't really good for the memory.
        self.parent = parent

        # find out in what interval we are
        interval_number = -1
        for interval in range(len(self.safe_intervals)):
            if self.safe_intervals[interval][0] <= t and self.safe_intervals[interval][1] >= t:
                interval_number = interval
        if interval_number >= 0:
            self.interval = interval_number
            
        else:
            raise ValueError('With this time ' + str(self.time) + ' the Search State ' + str(self.cfg) + ' can not be generated')
        
        if self.cfg in walls:
            raise ValueError('Your Search State is in a wall')
            
    # Where can our agent move to (without taking moving obstacles into account)
    def possible_moves(self):
        all_moves = []
           
        # Moving left
        if self.cfg[0]-1 >= 0 and [self.cfg[0]-1,self.cfg[1]] not in walls:
            all_moves.append([self.cfg[0]-1,self.cfg[1]])        
            
        # Moving down
        if self.cfg[1]-1 >= 0 and [self.cfg[0],self.cfg[1]-1] not in walls:
            all_moves.append([self.cfg[0],self.cfg[1]-1])       
        
        # Moving right
        if self.cfg[0]+1 < size and [self.cfg[0]+1,self.cfg[1]] not in walls:
            all_moves.append([self.cfg[0]+1,self.cfg[1]])
        
        # Moving up
        if self.cfg[1]+1 < size and [self.cfg[0], self.cfg[1]+1] not in walls:
            all_moves.append([self.cfg[0], self.cfg[1]+1])
        
        # here we construct a dummy node to ensure that no vehicle drives through us when we are in our first goal node
        if phase == 1 and self.cfg == first_goal:
            all_moves.append([-1,-1])
        return all_moves
    
    def getSuccessors(self):
        successors = []
        
        for m in self.possible_moves():
            new_cfg = Configuration(m, dynamic_obstacles)
            m_time = 1
                
            start_t = self.time + m_time 
            end_t = self.safe_intervals[self.interval][1] + m_time
            
            # We now iterate through all possible safe intervals of the cfg we want to move to
            for i in range(len(new_cfg.safe_intervals)):

                # If we take to long to reach this interval or are to fast we disregard this interval
                if new_cfg.safe_intervals[i][0] > end_t or new_cfg.safe_intervals[i][1] < start_t:
                    continue
                
                # This approach should only work for our fixed setting with the 4 movement and cost 1. Not sure if it also works in other settings
                # This is just a workaround so far
                
                # This is the earliest arriving time in the interval
                t = max(start_t, new_cfg.safe_intervals[i][0])
                
                # This is only valid if there is no dynamic obstacle that uses the edge at the same time
                obstacle_crosses = False
                for obstacle in dynamic_obstacles:
                    if t > 0 and t < len(obstacle):
                        if obstacle[t-1] == new_cfg.cfg and obstacle[t] == self.cfg:

                            obstacle_crosses = True

                if not obstacle_crosses:
                    successors.append(SearchState(new_cfg, math.inf, math.inf, i, t, SearchState(self.Configuration, self.g, self.f, self.interval, self.time, self.parent)))                   
        return successors
    
    # Manhattan heuristic
    def heuristic(self, goal):
        return math.fabs(self.cfg[0] - goal[0]) + math.fabs(self.cfg[1] - goal[1])
    
    
# Here we want to find a "good" stop for every vehicle entering the station
# We have to make sure that we plan the paths for the vehicles in the order they arrive at the station
def stop_assignment(wait, entering_time, allocation_type = 'random'):
    
    # find all possible safe intervals for the stops
    safe_intervals = []
    
    for stop in stops:
        times_obstacles_in_cfg = []
        # Here we collect all the timesteps in which an obstacle passes our stop
        for obstacle_number in range(len(dynamic_obstacles)):
            for i in range(len(dynamic_obstacles[obstacle_number])):
                if dynamic_obstacles[obstacle_number][i] == stop and i not in times_obstacles_in_cfg:
                    times_obstacles_in_cfg.append(i)
                
        # If no obstacles pass our stop we return an empty list
        if len(times_obstacles_in_cfg) < 1:
            safe_intervals.append(([[0,math.inf]], stop))
            continue
        
        intervals = []
        sorted_times = sorted(times_obstacles_in_cfg)
        
        if sorted_times[0] > waiting_time and (math.fabs(start_state[0] - stop[0]) + math.fabs(start_state[1] - stop[1]) + waiting_time + entering_time) < sorted_times[0]:
            intervals.append([0,sorted_times[0] - waiting_time])
            
        for i in range(len(sorted_times) - 1):
            if sorted_times[i+1] - sorted_times[i] > waiting_time + 1 and (math.fabs(start_state[0] - stop[0]) + math.fabs(start_state[1] - stop[1]) + waiting_time + entering_time) < sorted_times[i]:
                interval_start = sorted_times[i] + 1
                interval_end = sorted_times[i+1] - waiting_time
                intervals.append([interval_start, interval_end])
        intervals.append([sorted_times[-1] + 1, math.inf])
    
        safe_intervals.append((intervals, stop))
    # return a random stop that has a safe interval that is long enough for us to visit
    if allocation_type == 'random':
        possible_stops = []
        for element in safe_intervals:
            if len(element[0]) > 0:
                possible_stops.append(element[1])
        return possible_stops[random.randrange(0,len(possible_stops))]
    
    # return the stop that has the earliest safe interval iterating through the list front to back
    if allocation_type == 'earliest back':
        earliest_time = math.inf
        best_stop = []
        for element in safe_intervals:
            # do we have safe intervals?
            if len(element[0]) > 0:
                # is the start of our first safe interval earlier than our so far earliest interval?
                if element[0][0][0] < earliest_time:
                    earliest_time = element[0][0][0]
                    best_stop = element[1]
        return best_stop
    
    # return the stop that has the earliest safe interval iterating through the list back to front  
    if allocation_type == 'earliest front':
        earliest_time = math.inf
        best_stop = []
        for element in reversed(safe_intervals):
            # do we have safe intervals?
            if len(element[0]) > 0:
                # is the start of our first safe interval earlier than our so far earliest interval?
                if element[0][0][0] < earliest_time:
                    earliest_time = element[0][0][0]
                    best_stop = element[1]
        return best_stop
    
    # Take the stop in the front of the station and then fill all other stops up. 
    # Start in front again when you arrive in the stop in the back of the statio
    if allocation_type == 'ordered front to back':
        number_vehicles = len(dynamic_obstacles)
#        print(stops[-((number_vehicles+1)%len(stops))])
#        print('\n')
        return stops[-((number_vehicles+1)%len(stops))]
    
    # Same as "ordered front to back" only that you start in the back of the station and work your way forward
    if allocation_type == 'ordered back to front':
        number_vehicles = len(dynamic_obstacles)
        return stops[(number_vehicles%len(stops))]                                                                                   #   
                                                                                                                                     #
######################################################################################################################################
    
############################################ The A* Algorithm ########################################################################
def A_star(start_state, goal, time):                                                                                                 #   
    StartConfiguration = Configuration(start_state, dynamic_obstacles)                                                               #
    StartSearchState = SearchState(StartConfiguration, g = 0, t = time)
    
    StartSearchState.f = StartSearchState.heuristic(goal)
    
    # The OPEN list is a tuple of Search States and their respective f-value
    OPEN = [StartSearchState]
    
    expand_next = OPEN[0]
    expanded = [] # full list of all SearchStates
    expanded_cfg = [] # list only of expanded configurations

    while goal not in expanded_cfg:
        
        
        if len(OPEN) < 1:
            raise ValueError('For this start and goal configuration no path could be found')
            
        
        state_index = 0
        for state in range(len(OPEN)):
            if OPEN[state].f < OPEN[state_index].f:
                state_index = state
                
        expand_next = OPEN.pop(state_index)
        
        successors = expand_next.getSuccessors()
        
        for successor in successors:
            visited = False
            visited_nr = -1
            
            in_expanded = False
            # Check if the State was already expanded        
            for state_in_expanded in expanded:
                if state_in_expanded.cfg == successor.cfg and state_in_expanded.interval == successor.interval:
                    in_expanded = True
            if in_expanded:
                continue
            
            
            # Check if State is already in OPEN
            for state_in_open in OPEN:
                if state_in_open.cfg == successor.cfg and state_in_open.interval == successor.interval:
                    visited = True
                    visited_nr = OPEN.index(state_in_open)
                    
            # Update cost of state if the new cost is smaller than the existing cost
            if visited and OPEN[visited_nr].g > expand_next.time + 1:
                OPEN[visited_nr].g = expand_next.time + 1
                OPEN[visited_nr].time = successor.time
                OPEN[visited_nr].f = OPEN[visited_nr].g + OPEN[visited_nr].heuristic(goal)
                OPEN[visited_nr].parent = expand_next
            
            # If it was not visited calculate g and f
            if not visited:
                successor.g = expand_next.time + 1
                successor.f = successor.g + successor.heuristic(goal)
                OPEN.append(successor)
        
        expanded.append(expand_next)
        expanded_cfg.append(expand_next.cfg)

    
    # Now we have to construct our graph from the parents
    state = expanded[-1]
    path = [state.cfg]
    time_to_goal = state.time-time
    Check = False
    while not Check:
        Check = (state.parent.cfg == start_state and state.parent.time == time)
        if not Check:
            
            for i in range(state.time-state.parent.time):
                path.append(state.parent.cfg)
        else:
            for i in range(state.time-time):
                path.append(state.parent.cfg)
        state = state.parent

    path.reverse()
                                                                                  #
    return (path, time_to_goal)                                                                                                      #
######################################################################################################################################

#################### This uses A* to calculate the shortest path from start to stop to exit ##########################################
                                                                                                                                     #
def shortest_path(start_time):                                                                                                       #           
    A_star_1 = to_first_goal(start_time)
    first_path = A_star_1[0]
    A_star_2 = to_second_goal(start_time + len(first_path)-1)
    second_path = A_star_2[0]
    
    time_to_first_goal = A_star_1[1]-1 #We need this -1 here because of the dummy node we use
    time_to_second_goal = A_star_2[1]
    return (combine_two_path(first_path, second_path, start_time), time_to_first_goal, time_to_second_goal, first_goal)

# Gives us the path from our start state to our first goal
def to_first_goal(start_time):
    global phase
    phase = 1
    return A_star(start_state, [-1,-1], start_time)

# Gives us the path from our first goal to our second goal
def to_second_goal(t):
    global phase
    phase = 2
    if first_goal == second_goal:
        return ([], 0)
    return A_star(first_goal, second_goal,t+waiting_time-2)

# Gives us the complete path start -> first goal -> second goal
def combine_two_path(first_path, second_path, start_time):
    
    first_path = first_path[:-1]
    first_path.append(first_goal)
    # Take the waiting time at first goal into account
    for i in range(waiting_time-2):
        first_path.append(first_goal)
    
    for i in range(start_time):
        first_path.insert(0, [math.inf, math.inf])                                                                                   #   
    return first_path + second_path[1:]                                                                                              #
######################################################################################################################################




######################################  Here We initialize the Algorithm #############################################################
                                                                                                                                     #       
                                                                                                                                     #
global start_state
global first_goal
global second_goal
global waiting_time
global walls
global dynamic_obstacles
global size
global phase
global stops

start_state = [0,0]
first_goal = [0,0]
second_goal = [0,0]
waiting_time = 0
walls = []
dynamic_obstacles = []
size = 0
phase = 0
stops = []


def solve(start, goal_1, goal_2, wait, walls_in_model, obstacles, size_of_model, start_time, all_stops = [], assignment_stops = None, is_with_information = False):
    global start_state
    global first_goal
    global second_goal
    global waiting_time
    global walls
    global dynamic_obstacles
    global size
    global stops
    
    start_state = start
    stops = all_stops
    second_goal = goal_2
    waiting_time = wait
    walls = walls_in_model
    dynamic_obstacles = obstacles
    size = size_of_model
    first_goal = goal_1
    
    
    if assignment_stops != None:
        first_goal = stop_assignment(wait, start_time, assignment_stops)
        
    if is_with_information:
        return shortest_path(start_time)
    solve = A_star(start, first_goal, start_time)
    
    path = solve[0]
    for i in range(start_time):
        path.insert(0, [math.inf, math.inf])  
    time = solve[1]
    return (path, time, first_goal)


def update(start, goal_1, goal_2, wait, walls_in_model, obstacles, size_of_model, start_time, our_phase, is_with_information = False):
    global start_state
    global first_goal
    global second_goal
    global waiting_time
    global walls
    global dynamic_obstacles
    global size
    
    # if the vehicle is on its way to a stop we can just use the solve function
    if our_phase == 1:
        start_state = start
        first_goal = goal_1
        walls = walls_in_model
        dynamic_obstacles = obstacles
        size = size_of_model
        
        
        solve = A_star(start, goal_1, start_time)
        path = solve[0]
        for i in range(start_time):
            path.insert(0, [math.inf, math.inf])  
        time = solve[1]
        return (path, time)
    
    # if the vehcile is on its way to the exit we have to update the globals and then use A_star
    if our_phase == 2:
        phase = 2
        walls = walls_in_model
        dynamic_obstacles = obstacles
        size = size_of_model
        start_state = start
        
        return A_star(start, goal_2, start_time)
    

######################################################################################################################################