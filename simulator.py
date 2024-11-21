import random
import csv
import math
from matplotlib import pyplot as plt
import numpy as np

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
virality = 1    # probability that a neighbor cell is infected in 
                  # each time step                                                  

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
        if self.time < 1 or not self.state == "I" :
            self.time += 1
            return
        for i in adjacent_cells:
            if i.state == "S" and random.random() <= virality:
                i.infect()
                    
        
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
        

        plt.imshow(image)  # display the map
    
    def time_step(self):
        for i in self.cells.values():
            i.process(self.adjacent_cells(i.x, i.y))
        self.display()
        
    def adjacent_cells(self, x, y): # Step 2.2
        adjacentCells = []
        if (x, y+1) in self.cells.keys(): #Just realized you dont actually need to care about y == 0 because it shouldn't have a key at that point anyway
            adjacentCells.append(self.cells[(x, y+1)])
        if (x, y-1) in self.cells.keys(): 
            adjacentCells.append(self.cells[(x, y-1)])
        if (x+1, y) in self.cells.keys(): 
            adjacentCells.append(self.cells[(x+1, y)])
        if (x-1, y) in self.cells.keys(): 
            adjacentCells.append(self.cells[(x-1, y)])
        
        return adjacentCells
            
            

def read_map(filename):
    m = Map()
    file = open(filename, "r")
    data_reader = csv.reader(file)
    for line in data_reader:
        m.add_cell(Cell(line[0], line[1])) #idk why but this legit only works with csvreader for me was using for line in file
    
    file.close()
    return m



"""if __name__ == "__main__":
    image = read_map("nyc_map.csv")
    image.display()
"""