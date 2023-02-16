#The A* algorithm for finding minimum distance between two points with optimal computational time
#A class has been defined to track indices, block, f, g and h values
#The class comparison with itself i based on its indices
#A set has been defined to check the points that have been visited
#The algorithm has been tested upto 800X800X800 grid. With an answer in 1hr 50 min.
#The problem with bigger grid is lack of heap memory for the program.
#The algorithm can work for bigger grid if we remove an initial grid, but then we will
#not have a return path list. Or we can put the grid on a text file. and read it. 

import math
import numpy as np
import datetime
from builtins import isinstance

#Entered number is not a positive integer or whole number
class Err1_posnum(Exception):
    pass

#Start point is not inside the grid.
class Err2_originout(Exception):
    pass

#End point is not inside the grid.
class Err3_endout(Exception):
    pass

#Zero grid size
class Err4_zerogrid(Exception):
    pass

#Prevent code from running into infinite loop
class Err5_infiloop(Exception):
    pass

#Printing ending time as an exception
class Err6_finish(Exception):
    pass

class gridpoint:
    
    def __init__(self, value, x, y, z):
        self.h = value
        self.g = value
        self.f = self.g + self.h
        self.origin = (-1,-1,-1)
        self.displace = -1
        self.indices = (x,y,z)
        self.check = "u"
        self.block = "u"
        #self.neighbours = 26
        
    def __eq__(self,other):
        return (self.indices == other.indices)
        
    def __lt__(self, other):
        return (self.indices < other.indices)
    
    def __ne__(self,other):
        return (not self.indices == other.indices)
    
    def __repr__(self):
        return (str(self.indices[0])+","+str(self.indices[1])+","+str(self.indices[2])+": "+str(self.f))#+":"+str(self.f)+":"+str(self.g)+":"+str(self.h))
    
    def __str__(self):
        return (str(self.indices[0])+","+str(self.indices[1])+","+str(self.indices[2]))

def get_gp_f(gp):
    return gp.f 

def getinput():
    try:        
        x = int(input("Enter the number of gridpoints in x direction."))
        y = int(input("Enter the number of gridpoints in y direction."))
        z = int(input("Enter the number of gridpoints in z direction."))
    
        i_start = int(input("Enter the x-value of start point."))
        j_start = int(input("Enter the y-value of start point."))
        k_start = int(input("Enter the z-value of start point."))
    
        i_stop = int(input("Enter the x-value of stop point."))
        j_stop = int(input("Enter the y-value of stop point."))
        k_stop = int(input("Enter the z-value of stop point."))
    
        if (x < 0) and (y < 0) and (z < 0) and (i_start < 0) and (j_start < 0) and (k_start < 0) and (i_stop < 0) and (j_stop < 0) and (k_stop < 0): 
            raise Err1_posnum
        elif (i_start>x) or (j_start>y) or (k_start>z):
            raise Err2_originout
        elif (i_stop>x) or (j_stop>y) or (k_stop>z):
            raise Err3_endout
        elif (x == 0) and (y == 0) and (z == 0):
            raise Err4_zerogrid
        else:
            return (x,y,z,i_start,j_start,k_start,i_stop,j_stop,k_stop)
    except Err1_posnum:
        print("Error 001 - Please enter a positive integer or whole number.")
    except Err2_originout:
        print("Error 002 - Please enter a start point inside the grid.")
    except Err3_endout:
        print("Error 003 - Please enter a stop point inside the grid.")
    except Err4_zerogrid:
        print("Error 003 - The grid should have some dimensions.")
        
def makegrid(x,y,z,i_start,j_start,k_start,i_stop,j_stop,k_stop):
    grid1 = np.zeros((x,y,z))
    grid = grid1.tolist()
    grid[i_start][j_start][k_start] = gridpoint(1,i_start,j_start,k_start)
    grid[i_start][j_start][k_start].origin = (i_start,j_start,k_start)
    grid[i_start][j_start][k_start].g = 0
    grid[i_start][j_start][k_start].h = round(2*math.sqrt((i_start - i_stop)**2 + (j_start - j_stop)**2 + (k_start - k_stop)**2),3)
    grid[i_start][j_start][k_start].f = grid[i_start][j_start][k_start].g + grid[i_start][j_start][k_start].h
    grid[i_start][j_start][k_start].displace = 0
    grid[i_stop][j_stop][k_stop] = gridpoint(1,i_stop,j_stop,k_stop)
    grid[i_stop][j_stop][k_stop].origin = (i_stop,j_stop,k_stop)
    grid[i_stop][j_stop][k_stop].g = round(((i_start - i_stop)**2 + (j_start - j_stop)**2 + (k_start - k_stop)**2),3)
    grid[i_stop][j_stop][k_stop].h = 0
    grid[i_stop][j_stop][k_stop].f = grid[i_stop][j_stop][k_stop].g + grid[i_stop][j_stop][k_stop].h
    grid[i_stop][j_stop][k_stop].displace = euclidean(grid[i_stop][j_stop][k_stop], grid[i_start][j_start][k_start])
    return grid           

def make_neighbour_gridpoint(grid,x,y,z,i_start,j_start,k_start,i_stop,j_stop,k_stop):
    for l in range (max(x-2,0),min(x+3,len(grid))):
        for m in range (max(y-2,0),min(y+3, len(grid[0]))):
            for n in range (max(z-2,0),min(z+3,len(grid[0][0]))):
                if (isinstance(grid[l][m][n], gridpoint) == False):
                    if (l == i_start) and (m == j_start) and (n == k_start):
                        grid[l][m][n] = gridpoint(1,l,m,n)
                        grid[l][m][n].origin = (l,m,n)
                        grid[l][m][n].g = 0
                        grid[l][m][n].h = round(2*math.sqrt((i_start - i_stop)**2 + (j_start - j_stop)**2 + (k_start - k_stop)**2),3)
                        grid[l][m][n].f = grid[l][m][n].g + grid[l][m][n].h
                        grid[l][m][n].displace = 0
                    elif (l == i_stop) and (m == j_stop) and (n == k_stop):
                            grid[l][m][n] = gridpoint(1,l,m,n)
                            grid[l][m][n].origin = (l,m,n)
                            grid[l][m][n].g = round(((i_start - i_stop)**2 + (j_start - j_stop)**2 + (k_start - k_stop)**2),3)
                            grid[l][m][n].h = 0
                            grid[l][m][n].f = grid[l][m][n].g + grid[l][m][n].h
                            grid[l][m][n].displace = euclidean(grid[l][m][n], grid[i_start][j_start][k_start])
                    else:
                        grid[l][m][n] = gridpoint(round(((len(grid)**2)+(len(grid[0])**2)+(len(grid[0][0])**2)),3),l,m,n)

#Function to get euclidean distance - L-2 norm   
def euclidean(a,b):
    displace = round(math.sqrt((a.indices[0]-b.indices[0])**2 +(a.indices[1]-b.indices[1])**2+(a.indices[2]-b.indices[2])**2),3)
    return displace

#Function to get manhattan distance - adding all dimension    
def manhattan(a,b):
    displace = (abs(a.indices[0]-b.indices[0])+abs(a.indices[1]-b.indices[1])+abs(a.indices[2]-b.indices[2]))
    return displace

def change_gridvalue(grid,checklist,i_curr,j_curr,k_curr,origin,end,disptype):
    i_stop,j_stop,k_stop = end.indices[0], end.indices[1], end.indices[2]
    if disptype == "e":
        grid[i_curr][j_curr][k_curr].h = euclidean(grid[i_curr][j_curr][k_curr], grid[i_stop][j_stop][k_stop])
    elif disptype == "m":
        grid[i_curr][j_curr][k_curr].h = manhattan(grid[i_curr][j_curr][k_curr], grid[i_stop][j_stop][k_stop])
    grid[i_curr][j_curr][k_curr].origin = (origin.indices[0], origin.indices[1], origin.indices[2])
    grid[i_curr][j_curr][k_curr].check = "c"
    grid[i_curr][j_curr][k_curr].f = grid[i_curr][j_curr][k_curr].g + grid[i_curr][j_curr][k_curr].h
    add_list(grid,checklist,i_curr,j_curr,k_curr)


def xneighbours(grid,checklist,origin,end,disptype):
    i,j,k = origin.indices[0], origin.indices[1], origin.indices[2]
    #Only the g value can change by getting reduced if the point is reached by a shorter
    #path. So check if with the new g value the f value is reduced. If yes, update
    #Check if the point to be checked is within the grid or not
    #check if the neighbours are in grid checklist or not
    if (i > 0) and (((origin.g + 1) + grid[i-1][j][k].h) < grid[i-1][j][k].f):
        grid[i-1][j][k].g = grid[i][j][k].g + 1
        change_gridvalue(grid,checklist,i-1,j,k,origin,end,disptype)
    if (i<len(grid)-1) and (((origin.g + 1) + grid[i+1][j][k].h) < grid[i+1][j][k].f):
        grid[i+1][j][k].g = grid[i][j][k].g + 1
        change_gridvalue(grid,checklist,i+1,j,k,origin,end,disptype)

def yneighbours(grid,checklist,origin,end,disptype):
    i,j,k = origin.indices[0], origin.indices[1], origin.indices[2]
    #Only the g value can change by getting reduced if the point is reached by a shorter
    #path. So check if with the new g value the f value is reduced. If yes, update
    #Check that the point to be checked is within the grid
    #check if the neighbours are in grid checklist or not
    if (j > 0) and (((origin.g + 1) + grid[i][j-1][k].h) < grid[i][j-1][k].f):
        grid[i][j-1][k].g = origin.g + 1
        change_gridvalue(grid,checklist,i,j-1,k,origin,end,disptype)
        
    if (j<len(grid[0])-1) and (((origin.g + 1) + grid[i][j+1][k].h) < grid[i][j+1][k].f):
        grid[i][j+1][k].g = origin.g + 1
        change_gridvalue(grid,checklist,i,j+1,k,origin,end,disptype)
    
def zneighbours(grid,checklist,origin,end,disptype):
    i,j,k = origin.indices[0], origin.indices[1], origin.indices[2]
    #Only the g value can change by getting reduced if the point is reached by a shorter
    #path. So check if with the new g value the f value is reduced. If yes, update
    #Check that the point to be checked is within the grid
    #check if the neighbours are in grid checklist or not
    if (k > 0) and (((origin.g + 1) + grid[i][j][k-1].h) < grid[i][j][k-1].f):
        grid[i][j][k-1].g = origin.g + 1
        change_gridvalue(grid,checklist,i,j,k-1,origin,end,disptype)
        
    if (k<len(grid[0][0])-1) and (((origin.g + 1) + grid[i][j][k+1].h) < grid[i][j][k+1].f):
        grid[i][j][k+1].g = origin.g + 1
        change_gridvalue(grid,checklist,i,j,k+1,origin,end,disptype)
        
def btmneighbours(grid,checklist,origin,end,disptype):
    i,j,k = origin.indices[0], origin.indices[1], origin.indices[2]
    #Only the g value can change by getting reduced if the point is reached by a shorter
    #path. So check if with the new g value the f value is reduced. If yes, update
    #The grid dimensions are assumed to be equal and sqrt(3) = 1.732
    #layer_top: z+1, right:x-1, top:y+1 
    #Check that the point to be checked is within the grid
    #check if the neighbours are in grid checklist or not
    #top left
    if (i>0) and (j<len(grid[0])-1) and (k > 0) and (((origin.g + 1.732) + grid[i-1][j+1][k-1].h) < grid[i-1][j+1][k-1].f):
        grid[i-1][j+1][k-1].g = round((origin.g + 1.732),3)
        change_gridvalue(grid,checklist,i-1,j+1,k-1,origin,end,disptype)
        
    #top middle
    if (j<len(grid[0])-1) and (k > 0) and (((origin.g + 1.414) + grid[i][j+1][k-1].h) < grid[i][j+1][k-1].f):
        grid[i][j+1][k-1].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i,j+1,k-1,origin,end,disptype)
        
    #top right
    if (i<len(grid)-1) and (j<len(grid[0])-1) and (k > 0) and (((origin.g + 1.732) + grid[i+1][j+1][k-1].h) < grid[i+1][j+1][k-1].f):
        grid[i+1][j+1][k-1].g = round((origin.g + 1.732),3)
        change_gridvalue(grid,checklist,i+1,j+1,k-1,origin,end,disptype)
        
    #side left
    if (i>0) and (j<len(grid[0])-1) and (k > 0) and (((origin.g + 1.414) + grid[i-1][j][k-1].h) < grid[i-1][j][k-1].f):
        grid[i-1][j][k-1].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i-1,j,k-1,origin,end,disptype)
        
    #side right
    if (i<len(grid)-1) and (j<len(grid[0])-1) and (k > 0) and (((origin.g + 1.414) + grid[i+1][j][k-1].h) < grid[i+1][j][k-1].f):
        grid[i+1][j][k-1].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i+1,j,k-1,origin,end,disptype)
        
    #bottom left
    if (i>0) and (j>0) and (k > 0) and (((origin.g + 1.732) + grid[i-1][j-1][k-1].h) < grid[i-1][j-1][k-1].f):
        grid[i-1][j-1][k-1].g = round((origin.g + 1.732),3)
        change_gridvalue(grid,checklist,i-1,j-1,k-1,origin,end,disptype)
        
    #bottom middle
    if (j > 0) and (k > 0) and (((origin.g + 1.414) + grid[i][j-1][k-1].h) < grid[i][j-1][k-1].f):
        grid[i][j-1][k-1].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i,j-1,k-1,origin,end,disptype)
        
    #bottom right
    if (i<len(grid)-1) and (j > 0) and (k > 0) and (((origin.g + 1.732) + grid[i+1][j-1][k-1].h) < grid[i+1][j-1][k-1].f):
        grid[i+1][j-1][k-1].g = round((origin.g + 1.732),3)
        change_gridvalue(grid,checklist,i+1,j-1,k-1,origin,end,disptype)
    
def middleneighbours(grid,checklist,origin,end,disptype):
    i,j,k = origin.indices[0], origin.indices[1], origin.indices[2]
    #Only the g value can change by getting reduced if the point is reached by a shorter
    #path. So check if with the new g value the f value is reduced. If yes, update
    #The grid dimensions are assumed to be equal and sqrt(3) = 1.732
    #layer_top: z+1, right:x-1, top:y+1 
    #Check that the point to be checked is within the grid
    #check if the neighbours are in grid checklist or not
    #top left
    if (i > 0) and (j < len(grid[0])-1) and (((origin.g + 1.414) + grid[i-1][j+1][k].h) < grid[i-1][j+1][k].f):
        grid[i-1][j+1][k].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i-1,j+1,k,origin,end,disptype)
        
    #top right
    if (i < len(grid)-1) and (j < len(grid[0])-1) and (((origin.g + 1.414) + grid[i+1][j+1][k].h) < grid[i+1][j+1][k].f):
        grid[i+1][j+1][k].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i+1,j+1,k,origin,end,disptype)
        
    #bottom left
    if (i > 0) and (j > 0) and (((origin.g + 1.414) + grid[i-1][j-1][k].h) < grid[i-1][j-1][k].f):
        grid[i-1][j-1][k].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i-1,j-1,k,origin,end,disptype)
        
    #bottom right
    if (i < len(grid)-1) and (j > 0) and (((origin.g + 1.414) + grid[i+1][j-1][k].h) < grid[i+1][j-1][k].f):
        grid[i+1][j-1][k].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i+1,j-1,k,origin,end,disptype)
        
def topneighbours(grid,checklist,origin,end,disptype):
    i,j,k = origin.indices[0], origin.indices[1], origin.indices[2]
    #Only the g value can change by getting reduced if the point is reached by a shorter
    #path. So check if with the new g value the f value is reduced. If yes, update
    #The grid dimensions are assumed to be equal and sqrt(3) = 1.732
    #layer_top: z+1, right:x-1, top:y+1 
    #Check that the point to be checked is within the grid
    #check if the neighbours are in grid checklist or not
    #top left
    if (i>0) and (j<len(grid[0])-1) and (k<len(grid[0][0])-1) and (((origin.g + 1.732) + grid[i-1][j+1][k+1].h) < grid[i-1][j+1][k+1].f):
        grid[i-1][j+1][k+1].g = round((origin.g + 1.732),3)
        change_gridvalue(grid,checklist,i-1,j+1,k+1,origin,end,disptype)
    
    #top middle
    if (j<len(grid[0])-1) and (k<len(grid[0][0])-1) and (((origin.g + 1.414) + grid[i][j+1][k+1].h) < grid[i][j+1][k+1].f):
        grid[i][j+1][k+1].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i,j+1,k+1,origin,end,disptype)
    
    #top right
    if (i<len(grid)-1) and (j<len(grid[0])-1) and (k<len(grid[0][0])-1) and (((origin.g + 1.732) + grid[i+1][j+1][k+1].h) < grid[i+1][j+1][k+1].f):
        grid[i+1][j+1][k+1].g = round((origin.g + 1.732),3)
        change_gridvalue(grid,checklist,i+1,j+1,k+1,origin,end,disptype)
        
    #side left
    if (i>0) and (k<len(grid[0][0])-1) and (((origin.g + 1.414) + grid[i-1][j][k+1].h) < grid[i-1][j][k+1].f):
        grid[i-1][j][k+1].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i-1,j,k+1,origin,end,disptype)
    
    #side right
    if (i<len(grid)-1) and (k<len(grid[0][0])-1) and (((origin.g + 1.414) + grid[i+1][j][k+1].h) < grid[i+1][j][k+1].f):
        grid[i+1][j][k+1].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i+1,j,k+1,origin,end,disptype)
    
    #bottom left
    if (i>0) and (j>0) and (k<len(grid[0][0])-1) and (((origin.g + 1.732) + grid[i-1][j-1][k+1].h) < grid[i-1][j-1][k+1].f):
        grid[i-1][j-1][k+1].g = round((origin.g + 1.732),3)
        change_gridvalue(grid,checklist,i-1,j-1,k+1,origin,end,disptype)
        
    #bottom middle
    if (j>0) and (k<len(grid[0][0])-1) and (((origin.g + 1.414) + grid[i][j-1][k+1].h) < grid[i][j-1][k+1].f):
        grid[i][j-1][k+1].g = round((origin.g + 1.414),3)
        change_gridvalue(grid,checklist,i,j-1,k+1,origin,end,disptype)
        
    #bottom right
    if (i<len(grid)-1) and (j>0) and (k<len(grid[0][0])-1) and (((origin.g + 1.732) + grid[i+1][j-1][k+1].h) < grid[i+1][j-1][k+1].f):
        grid[i+1][j-1][k+1].g = round((origin.g + 1.732),3)
        change_gridvalue(grid,checklist,i+1,j-1,k+1,origin,end,disptype)

def add_list(grid,checklist,x,y,z):
    if grid[x][y][z] not in checklist:
        checklist.append(grid[x][y][z])
        
def path(grid,checklist,x,y,z,i_start,j_start,k_start):
    if (x == i_start) and (y == j_start) and (z == k_start):
        print((x,y,z))
        return        
    else:
        print((grid[x][y][z].origin[0],grid[x][y][z].origin[1],grid[x][y][z].origin[2]))
        path(grid,checklist,grid[x][y][z].origin[0],grid[x][y][z].origin[1],grid[x][y][z].origin[2],i_start,j_start,k_start)

def clean_checklist(checklist):
    length = len(checklist)
    list_remove = []
    for i in range(length):
        for j in range(length):
            if (checklist[i].indices == checklist[j].origin):
                list_remove.append(checklist[i])
    for ch in list_remove:
        if ch in checklist:
            checklist.remove(ch)       
        
def prog_run(x,y,z,i_start,j_start,k_start,i_stop,j_stop,k_stop):
    try:
        print(str(datetime.datetime.now()))
        grid = makegrid(x,y,z,i_start,j_start,k_start,i_stop,j_stop,k_stop)
        make_neighbour_gridpoint(grid,i_start,j_start,k_start,i_start,j_start,k_start,i_stop,j_stop,k_stop)
        make_neighbour_gridpoint(grid,i_stop,j_stop,k_stop,i_start,j_start,k_start,i_stop,j_stop,k_stop)
        checklist = []
        checklist.append(grid[i_start][j_start][k_start])
        end = grid[i_stop][j_stop][k_stop]
        disptype = "e"
        stop_infi = 2*x*y*z
        q = 0
        print(str(datetime.datetime.now()))
        while len(checklist) > 0:
            if q > 0:
                clean_checklist(checklist)
            sorted_list = sorted(checklist, key = get_gp_f)
            origin = sorted_list[0]
            make_neighbour_gridpoint(grid,origin.indices[0],origin.indices[1],origin.indices[2],i_start,j_start,k_start,i_stop,j_stop,k_stop)
            xneighbours(grid,checklist,origin,end,disptype)
            yneighbours(grid,checklist,origin,end,disptype)
            zneighbours(grid,checklist,origin,end,disptype)
            btmneighbours(grid,checklist,origin,end,disptype)
            middleneighbours(grid,checklist,origin,end,disptype)
            topneighbours(grid,checklist,origin,end,disptype)
            for ch in checklist:
                if (end.indices == ch.indices):
                    ans = ch
                    print("The answer for a {}X{}X{} grid.".format(x,y,z))
                    print("The minimum distance is: ", ans.f)
                    print("The last step location is: ", ans.origin)
                    print("The number of steps taken is: ", q)
                    raise Err6_finish
                q = q + 1
                if q == stop_infi:
                    print(sorted(checklist))
                    print(sorted(checklist, key = get_gp_f))
                    print("The total number of steps taken is:  ", q)
                    raise Err5_infiloop
                    break
    except Err1_posnum:
        print("Error 001 - Please enter a positive integer or whole number.")
    except Err2_originout:
        print("Error 002 - Please enter a start point inside the grid.")
    except Err3_endout:
        print("Error 003 - Please enter a stop point inside the grid.")
    except Err4_zerogrid:
        print("Error 003 - The grid should have some dimensions.")
    except Err5_infiloop:
        print(str(datetime.datetime.now())) 
        print("check the code it is running in infinite loop.")  
    except Err6_finish:
        print(str(datetime.datetime.now()))  

def mainrun():
  x,y,z,i_start,j_start,k_start,i_stop,j_stop,k_stop = getinput()
  prog_run(x,y,z,i_start,j_start,k_start,i_stop,j_stop,k_stop)


mainrun() 
