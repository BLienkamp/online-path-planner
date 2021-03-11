import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math

# Color Display
# Black = Wall
# Red = Agent


# Initializing number of dots
steps_between_points = 100

global paths
global walls_in_model
global size

paths = []
walls_in_model = []

# Creating dot class
class Dot(object):
    
    def __init__(self, x, y, agent):
        self.agent = agent
        self.x = x
        self.y = y
        self.pathsegment = 1
        self.velx = 0
        self.vely = 0
        self.steps_taken = 0


    def generate_vel(self):
        
        
        if self.pathsegment < len(paths[self.agent])-1:
            vel = np.array(paths[self.agent][self.pathsegment + 1]) - np.array(paths[self.agent][self.pathsegment])
        else:
            vel = [0,0]
        return vel

    def move(self):

        self.steps_taken += 1
        
        # If we reach a new vertex of our path we need to update the pathsegment we are in
        # and restart our counter
        if self.steps_taken == steps_between_points:
            self.steps_taken = 0
            self.pathsegment += 1

        # Move the dot in the needed direction
        self.x = self.x + self.generate_vel()[0]/steps_between_points
        self.y = self.y + self.generate_vel()[1]/steps_between_points
        return

class wall(object):
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
        
def visualize(paths_to_visualize, walls, size_model):
    global paths
    global walls_in_model
    global size
    
    paths = paths_to_visualize
    walls_in_model = walls
    size = size_model
    
    
         
            
    # Initializing dots
    dots = []
    
    # Initializing walls
    walls = [wall(walls_in_model[i][0], walls_in_model[i][1]) for i in range(len(walls_in_model))]
    
    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure()
    ax = plt.axes(xlim=(-0.5, size[0]+0.5), ylim=([size[1]-0.5, 20.5]))
    axes = plt.gca()
    axes.set_ylim([14, 20.5])
    
    # Setting the Plot
    ax.spines['bottom'].set_color('grey') 
    ax.spines['top'].set_color('grey') 
    ax.xaxis.label.set_color('white') 
    ax.tick_params(axis='x', colors='white')
    
    ax.spines['left'].set_color('grey') 
    ax.spines['right'].set_color('grey') 
    ax.xaxis.label.set_color('white') 
    ax.tick_params(axis='y', colors='white')
    
    plt.style.use('seaborn-whitegrid')
    
    minor_ticks_x = np.arange(-0.5, size[0], 1)
    minor_ticks_y = np.arange(size[1]-size[0]/2-0.5, 20+size[0]/2, 1)
    
    ax.set_xticks(minor_ticks_x)
    ax.set_yticks(minor_ticks_y)
    
    
    
    d, = ax.plot([dot.x for dot in dots],
                 [dot.y for dot in dots], 'ro', markersize = 5)
    
    ax.plot([wall.x for wall in walls],
                 [wall.y for wall in walls], 's', c = 'black', markersize = 8)
    
    
    # animation function.  This is called sequentially
    def animate(i):
        
        current_timestep = i/steps_between_points

        for dot in dots:
            if dot.pathsegment < len(paths[dot.agent])-1:
                dot.move()
            else:
                dots.remove(dot)

        for path in paths:
            if current_timestep == float(path[0]):
                dots.append(Dot(path[1][0], path[1][1], paths.index(path)))                
            
        d.set_data([dot.x for dot in dots],
                   [dot.y for dot in dots])
        

        return d,
    
    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, frames=25000, interval=5, blit = True, repeat = False)
    
    return anim






