from numpy import zeros # importing special matrix 

class SW_Matrix:
	'''This matrix given two strings populates itself according to the
	Smith-Waterman algorithm. Following the slides from the lecture, I named
	the methods involved in assiging a value to a cell Big D and small D. This
	should make it easier to understand what goes on in them.
	'''

	def __init__(self, s1, s2):
		''' class constructor '''
		self.matrix = zeros((len(s1),len(s2)))
		self.min_val = [0, ()]

	def small_d(self, char1, char2):
		'''Small D: determines whether two given characters match or not.
		If they match, method returns the bonus for matching, -2 in this case.
		Otherwise it returns penalty for mismatch, -1 in this case.
		'''
		if char1 == char2:
			#print 'match'
			return -2
		else:
			return 1

	def big_d(self, row, col):
		'''Big D: collects the values of all possible source cells, adds to
		them the result of Small D and returns the minimum value of these
		results and zero.
		'''
		string_comparison = self.small_d(s1[row],s2[col])
		above = self.matrix[row-1][col] + string_comparison
		left = self.matrix[row][col-1] + string_comparison
		diagonal = self.matrix[row-1][col-1] + string_comparison
		return min(0, above, left, diagonal)
	
	def populate(self):
		'''Method actually fills in matrix. Loops over rows and columns,
		assiging the result of Big D to them. It also (this was not covered in
		the slides), keeps track of the coordinates of the cell with the lowest
		value. This will become relevant later when we do traceback.
		'''
		rows = self.matrix.shape[0]
		cols = self.matrix.shape[1]
		for r in range(1, rows):
			for c in range(1, cols):
				val = self.big_d(r, c)
				self.matrix[r][c] = val

				if val <= self.min_val[0]: #checking if we have minimum value 
					self.min_val[0] = val
					self.min_val[1] = (r,c)
	
	def display(self):
		'''Slightly silly method, but useful if you want the possibility *not*
		to display the matrix that you arrive at as the result of populate().
		'''
		print 'For {0} and {1} we have the following matrix:\n'.format(s1, s2)
		print self.matrix
	
	def exists(self, pos):
		'''This method is for traceback. It determines if a given set of
		coordinates lies within the dimensions of the matrix. If that is not
		the case, method returns False. See the traceback methods for more
		details.
		'''
		#print pos
		if pos[0] > -1 and pos[1] > -1:
			return True
		else:
			return False

class SW_Aligner:
	'''This class uses two strings to create and populate a SW_Matrix object.
	It also has the methods and functionality to preform traceback over the
	matrix and generage an alignment. As my attempt to create a recursive
	traceback algorithm has failed, this one simply chooses a random minimum
	value to use as the next step. See below for details.
	'''
	def __init__(self, s1,s2):
		'''class constructor. '''
		self.matrix = SW_Matrix(s1,s2) #initialize matrix 
		self.matrix.populate() #populate it 
		self.matrix.display() # display it (comment this out if you want)

		self.min_val = self.matrix.min_val #stores coordinates of minimum 
		self.s1 = s1 #this and below line store the input strings 
		self.s2 = s2
		self.path = []  # list of pairings of indices 

	def generate_next(self, pos):
		'''Helper method that generates the next cell to feed into the align
		method, given a tuple of coordinates for the current cell. This goes in
		two stages:
		First, we collect all the possible continuations from a given cell,
		making sure that they are valid coordinates in the matrix and do not
		lie outside of it.
		We then sort the resulting list and choose the first member thereof,
		that has the minimum value. As mentioned earlier, we limit ourselves to
		the semi-random first member in the hopes of relatively consistently
		hitting the only cell with the minimum value.
		'''
		
		'''for convenience sake we assign the matrix to a shorter variable
		name. we also initiate a list of potential continuations as well as
		coordinate tuples for theoretically possible (but potentially
		out-of-bounds) candidates.
		'''
		cells, mat = [], self.matrix.matrix 
		diagonal = (pos[0]-1, pos[1]-1)		
		left = (pos[0], pos[1]-1)
		up = (pos[0]-1, pos[1])
		
		if self.matrix.exists(diagonal): #if there are cells on diagonal 
			cells.append((mat[pos[0]-1][pos[1]-1], diagonal))
			if self.matrix.exists(left):
				cells.append((mat[pos[0]][pos[1]-1], left))
			if self.matrix.exists(up):
				cells.append((mat[pos[0]-1][pos[1]], up))

			cells = sorted(cells) #sorting the list of cells 
			return cells[0][1] #choosing the minimum 
		else:
			return pos
		

		
	def align(self, pos, path=[]):
		'''This method is responsible for the actuall traceback.
		This is the method that I wanted to extend and make recursive, but
		succeeded only in a fairly limited degree.
		'''
		path.append(pos)
		if self.matrix.matrix[pos[0]][pos[1]] == 0:
			# ^ above we check whether we reached a zero
			self.path = path
		else: #if no zero reached, we continue collecting cells 
			next_pos = self.generate_next(pos)
			self.align(next_pos, path=path)
	
	def display(self):
		'''This method takes the work done by the align() method and converts
		it from a list of pairings of coordinates into a list of pairings of
		characters from the two strings.
		''' 
		path = self.path
		path.reverse() # putting pairings list in correct order for printing 
		approx =  [(s1[x[0]],s2[x[1]]) for x in path] #temporary list 
		alnmnt = [] #final output list 
		for pair in approx: #additional formatting for local mismatches 
			if pair[0] != pair[1]:
				alnmnt.append((pair[0], '-'))
				alnmnt.append(('-', pair[1]))
			else: # more typical case where chars match 
				alnmnt.append(pair)
		print '\nThis matrix yields the following allignment:\n'.format(s1, s2)
		print alnmnt


'''
The Testing Section.
The code below is just there to demonstrate how the alignment program works.
You should be able to modify it without much effect on the program as a whole
as long as you call on the right methods to do the right things.
'''

#s1= 'lounge' #uncomment and insert your own string if you want no prompt 
#s2= "s'allonger"
s1 = raw_input('Please give me a string to align\n')
s2 = raw_input('Please give me another string \n')
smith_w = SW_Aligner(s1,s2) #initiate the aligning class 
smith_w.align(smith_w.min_val[1]) #run aligning method
smith_w.display() # display the results 

