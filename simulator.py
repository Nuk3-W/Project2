import random
import math
from matplotlib import pyplot as plt
import numpy as np
import csv
import time

def image_example():
    '''should produce red,purple,green squares
    on the diagonal, over a black background'''
    # RGB indexes
    red,green,blue = range(3)
    # img array 
    # all zeros = black pixels
    # shape: (150 rows, 150 cols, 3 colors)
    img = np.zeros((150,150,3))
    for x in range(50):
        for y in range(50):
            # red pixels
            img[x,y,red] = 1.0
            # purple pixels
            # set 3 color components 
            img[x+50, y+50,:] = (.5,.0,.5)
            # green pixels
            img[x+100,y+100,green] = 1.0
    plt.imshow(img)

def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution 
    with the specified mean and standard deviation (sd) at
    position x.
    You do not have to understand how this function works exactly. 
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def pdeath(x, mean, sd):
    start = x-0.5
    end = x+0.5
    step =0.01    
    integral = 0.0
    while start<=end:
        integral += step * (normpdf(start,mean,sd) + normpdf(start+step,mean,sd)) / 2
        start += step            
    return integral    
    
recovery_time = 4 # recovery time in time-steps
virality = 0.2  # probability that a neighbor cell is infected in 
                  # each time step        
mean = 4
stdev = 1                                          

class Cell(object):

    def __init__(self,x, y):
        self.x = int(x)
        self.y = int(y)
        self.state = "S" # can be "S" (susceptible), "R" (resistant = dead), or 
                         # "I" (infected)
        self.time = 0
        
    def infect(self): # Step 2.1
        self.time = 0
        self.state = "I"


    def process(self, adjacent_cells): # Step 2.3
        if self.state == "I" and self.time >= 1:
            if self.time == recovery_time:
                self.state = "S"
                self.time == 0
            elif random.random() <= pdeath(self.time, mean, stdev): #The disease isn't spreading, they die instantly
                self.state = "R"    
                self.time = 0
            else:
                for i in adjacent_cells:
                    if i.state == "S" and random.random() <= virality:
                        i.infect()

                    
                self.time += 1
        
        else:
            self.time += 1
        
    
    
    
        
class Map(object):
    
    def __init__(self):
        self.height = 150
        self.width = 150           
        self.cells = {}

    def add_cell(self, cell): # Step 1.1 
        self.cells[(cell.x, cell.y)] = cell
        
    def display(self): # Step 1.3
        image = np.zeros((150,150,3),dtype='float')
        for i in self.cells.keys():
            if self.cells[i].state == "S":
                image[i[0], i[1]] = np.array([0.0,1.0,0.0])
            elif self.cells[i].state == "R":
                image[i[0], i[1]] = np.array([0.5,0.5,0.5])
            elif self.cells[i].state == "I":
                image[i[0], i[1]] = np.array([1.0,0.0,0.0])

        
        #plt.imshow(image)  # display the map
        
        #Nice feature for live updates
        
        plt.clf()
        plt.imshow(image)
        plt.axis('off')
        plt.pause(0.0001)
            
    
    def adjacent_cells(self, x,y): # Step 2.2
        adjacentCells = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in self.cells:
                adjacentCells.append(self.cells[(nx, ny)])
        return adjacentCells
    
    def time_step(self):
        for i in self.cells.values():
            i.process(self.adjacent_cells(i.x, i.y))
        self.display()

            
def read_map(filename):
    
    m = Map()
    
    with open(filename, "r") as f:
        data_reader = csv.reader(f)
        for i in data_reader:
            m.add_cell(Cell(i[0], i[1]))
    
    return m


if __name__ == "__main__":
    image = read_map("/Users/suwaidi/Downloads/nyc_map.csv")
    image.display()
    image.cells[ (39, 82)].infect()
    for i in range(100):
        image.time_step()
        time.sleep(0.2)
        
