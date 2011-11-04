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
		self.center = (gridPos[0] * cellDim[0], gridPos[1] * cellDim[1], gridPos[2] * cellDim[2]) 
		self.range = [(self.center[0] - cellDim[0] / 2, self.center[0] + cellDim[0] / 2),
					  (self.center[1] - cellDim[1] / 2, self.center[1] + cellDim[0] / 2),
					  (self.center[2] - cellDim[2] / 2, self.center[2] + cellDim[0] / 2)] 
										 
		self.children = [c for c in grid.children if isInside(self, c)]
		
			
			
	def isInside(self, child):
		if c.pos[0] in range(self.range[0][0], self.range[0][1]) and \
		   c.pos[1] in range(self.range[1][0], self.range[1][1]) and \
		   c.pos[2] in range(self.range[2][0], self.range[2][1]):
			   return True
		   
		return False
	
	def findNeighbors():
		 self.neighbors = [grid.cells[(self.gridPos[0], self.gridPos[1] + 1, self.gridPos[2])],
						  grid.cells[(self.gridPos[0], self.gridPos[1] - 1, self.gridPos[2])],
						  grid.cells[(self.gridPos[0] - 1, self.gridPos[1], self.gridPos[2])],
						  grid.cells[(self.gridPos[0] + 1, self.gridPos[1], self.gridPos[2])],
						  grid.cells[(self.gridPos[0], self.gridPos[1], self.gridPos[2] - 1)],
						  grid.cells[(self.gridPos[0], self.gridPos[1], self.gridPos[2] + 1)]]
		 
		   
		
				 
			
	

class Grid:
	
	def __init__(self, cellCounts, pos, dim, children):
		self.cells = {}
		self.pos = pos
		self.dim = dim #from objects bbox
		self.children = children
		self.cellCounts = cellCounts
	
		self.cellDim = [ round(dim[0] / cellCounts[0]), round(dim[1] / cellCounts[1]), 
						 round(dim[2] / cellCounts[2])]
		
		#build cells
		for x in range(0, cellCounts[0]):
			for y in range(0, cellCounts[1]):
				for z in range(0, cellCounts[2]):
				   self.cells[(x,y,z)] = Cell((x,y,z), self)
				   
		self.buildNeighborhood()
	
	def buildNeighborhood(self):
		[c.findNeighbors() for c in grid.cells.values()]
		
	
	def __str__(self):
		print(self.pos, self.dim, len(self.children))

class DataStore:
	pass

def register():
	pass

def unregister():
	pass
	