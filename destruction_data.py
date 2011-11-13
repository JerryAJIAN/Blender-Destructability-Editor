#cell contains: pieces of parent in range of cell size
# a cell size, a cell location(x,y,z), neighbors for quick access, retrieved from grid

#grid provides access to cells via x,y,z indexing, has a size and cell count to calculate cell sizes
#

#each object has a destruction dataset in context, to get it to game engine store it externally or maybe all custom properties will be converted ? could even work like that
#but for standalone mode no bpy may be used !
#and here no bge may be used, need to be clean data objects

class Cell:
    
    def __init__(self, gridPos, grid):
        self.gridPos = gridPos
        self.grid = grid
        cellDim = grid.cellDim
        self.center = ((gridPos[0] + 0.5) * cellDim[0] + grid.pos[0], 
                       (gridPos[1] + 0.5) * cellDim[1] + grid.pos[1], 
                       (gridPos[2] + 0.5) * cellDim[2] + grid.pos[2]) 
                       
        self.range = [(self.center[0] - cellDim[0] / 2, self.center[0] + cellDim[0] / 2),
                      (self.center[1] - cellDim[1] / 2, self.center[1] + cellDim[1] / 2),
                      (self.center[2] - cellDim[2] / 2, self.center[2] + cellDim[2] / 2)] 
                                         
        self.children = [c for c in grid.children if self.isInside(c)]
        self.count = len(self.children)
        print("Cell created: ", self.center, self.count)
        self.isGroundCell = False
    
    def integrity(self, intgr):
        if self.count == 0:
            return 0
        return len(self.children) / self.count > intgr     
            
    def isInside(self, c):
       # print("Child: ", c, c.worldPosition, self.range) 
        
        if c.worldPosition[0] >= self.range[0][0] and c.worldPosition[0] <= self.range[0][1] and \
           c.worldPosition[1] >= self.range[1][0] and c.worldPosition[1] <= self.range[1][1] and \
           c.worldPosition[2] >= self.range[2][0] and c.worldPosition[2] <= self.range[2][1]:
               return True
           
        return False
    
    def findNeighbors(self):
    
        back = None
        if self.gridPos[1] < self.grid.cellCounts[1] - 1:
            back = self.grid.cells[(self.gridPos[0], self.gridPos[1] + 1, self.gridPos[2])]
         
        front = None
        if self.gridPos[1] > 0:
            front = self.grid.cells[(self.gridPos[0], self.gridPos[1] - 1, self.gridPos[2])]
            
        left = None
        if self.gridPos[0] < self.grid.cellCounts[0] - 1:
            left = self.grid.cells[(self.gridPos[0] + 1, self.gridPos[1], self.gridPos[2])]
         
        right = None
        if self.gridPos[0] > 0:
            bottom = self.grid.cells[(self.gridPos[0] - 1, self.gridPos[1], self.gridPos[2])]
            
        top  = None
        if self.gridPos[2] < self.grid.cellCounts[2] - 1:
            top = self.grid.cells[(self.gridPos[0], self.gridPos[1], self.gridPos[2] + 1)]
         
        bottom = None
        if self.gridPos[2] > 0:
            bottom = self.grid.cells[(self.gridPos[0], self.gridPos[1], self.gridPos[2] - 1)]
            
        self.neighbors = [back, front, left, right, top, bottom]
                          
         
           
        
class Grid:
    
    def __init__(self, cellCounts, pos, dim, children):
        self.cells = {}
        #must start at upper left corner of bbox, that is the "origin" of the grid
        self.pos = (pos[0] - dim[0] / 2, pos[1] - dim[1] / 2, pos[2] - dim[2] / 2)
        self.dim = dim #from objects bbox
        self.children = children
        self.cellCounts = cellCounts
    
        self.cellDim = [ dim[0] / cellCounts[0], dim[1] / cellCounts[1], 
                         dim[2] / cellCounts[2]]
                         
        print("cell/grid dimension: ", self.cellDim, self.dim)
        
        #build cells
        for x in range(0, cellCounts[0]):
            for y in range(0, cellCounts[1]):
                for z in range(0, cellCounts[2]):
                   self.cells[(x,y,z)] = Cell((x,y,z), self)
                   
    #   self.buildNeighborhood()
    #    self.children = None
    #    self.pos = None
    #    self.dim =  None
    
    def buildNeighborhood(self):
        [c.findNeighbors() for c in self.cells.values()]
        #delete possible refs to bpy objects
    #    for c in self.cells.values():
    #        c.cellDim = None
    #        c.gridPos = None
    #        c.grid = None
        
    
    def __str__(self):
        return str(self.pos) + " " + str(self.dim) + " " + str(len(self.children))

class DataStore:
    backup = None
    grids = {}

#def register():
#   pass

#def unregister():
#   pass
    