from numpy import zeros

class SW_Matrix:
	def __init__(self, s1, s2):
		self.matrix = zeros((len(s1),len(s2)))
		self.min_val = [0, ()]

	def small_d(self, char1, char2):
		if char1 == char2:
			#print 'match'
			return -2
		else:
			return 1

	def big_d(self, row, col):
		string_comparison = self.small_d(s1[row],s2[col])
		#print string_comparison
		above = self.matrix[row-1][col] + string_comparison
		left = self.matrix[row][col-1] + string_comparison
		diagonal = self.matrix[row-1][col-1] + string_comparison
		return min(0, above, left, diagonal)
	
	def populate(self):
		rows = self.matrix.shape[0]
		cols = self.matrix.shape[1]
		for r in range(1, rows):
			for c in range(1, cols):
				val = self.big_d(r, c)
				self.matrix[r][c] = val
				if val <= self.min_val[0]:
					self.min_val[0] = val
					self.min_val[1] = (r,c)
	
	def display(self):
		print self.matrix
	
	def exists(self, pos):
		#print pos
		if pos[0] > -1 and pos[1] > -1:
			return True
		else:
			return False
class Cell:
	def __init__(self, value, coordinates, final=False):
		self.val = value
		self.coord = coordinates
		self.final = final

class SW_Aligner:
	def __init__(self, s1,s2):
		self.matrix = SW_Matrix(s1,s2)
		self.matrix.populate()
		self.matrix.display()
		self.min_val = self.matrix.min_val
		self.s1 = s1
		self.s2 = s2
		self.paths = [()]

	def generate_solutions(self, pos):
		# check for 
		cells, solutions, mat = [], [], self.matrix.matrix
		diagonal = (pos[0]-1, pos[1]-1)		
		left = (pos[0], pos[1]-1)
		up = (pos[0]-1, pos[1])
		
		if self.matrix.exists(diagonal):
			cells.append((mat[pos[0]-1][pos[1]-1], diagonal))
			if self.matrix.exists(left):
				cells.append((mat[pos[0]][pos[1]-1], left))
			if self.matrix.exists(up):
				cells.append((mat[pos[0]-1][pos[1]], up))

			cells = sorted(cells)
			min_cell = cells[0]

			if min_cell[0] == 0:
				solutions.append(Cell(min_cell[0], min_cell[1], final=True))
			else:
				solutions.append(Cell(min_cell[0], min_cell[1]))

			for c in cells[1:]:
				if c[0] <= min_cell[0]:
					if c[0] == 0:
						solutions.append(Cell(c[0], c[1], final=True))
					else:
						solutions.append(Cell(c[0], c[1])) 


					solutions.append(c[1])
		return solutions

		
	def foo(self, pos, path=[]):
		print 'up till now',path
		print 'exploring...', pos
		path.append(pos)
		if self.matrix.matrix[pos[0]][pos[1]] == 0:
			self.paths.append(path)
			print 'done with one loop'
			print self.paths
			return path[:-1]
		else:
			for solution in self.generate_solutions(pos):
				path = self.foo(solution, path=path)
	
	def display(self):
		print self.paths

s1= 'lounge'
s2= "s'allonger"
align = SW_Aligner(s1,s2)
print 'starting position',align.min_val[1]
align.foo(align.min_val[1])
#align.align((len(s1)-1, len(s2)-1))
align.display()

#matrix.populate()
#matrix.display()

