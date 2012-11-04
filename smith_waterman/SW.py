''' This is a sample implementation of the Smith-Waterman algorithm in an
attempt to adapt it to the alignment of different members of a declension
paradigm with the end goal of separating matching morphemes from those that
differ.
'''

from numpy import zeros

WORDS = [('help','unhelpful'), ('kamok','kamka')]
MATCH = 2
MISMATCH = -1
GAP = -1

def score(str1, str2):
	if str1 == str2:
		return MATCH
	else:
		return MISMATCH

class Allignments:

	def __init__(self, matrix, s1, s2):
		self.mat = matrix
		self.a = s1
		self.b = s2
		self.Paths = []

	def find_further_steps(self, x, y):
		steps = []  # this will be our output
		diag = self.mat[x-1][y-1]
		up = self.mat[x-1][y]
		left = self.mat[x][y-1]
		if x == 0:  # this is if we are at the top end of the matrix
			steps.append((x,y-1))
		elif y == 0:    # this is if we are at the left end of it
			steps.append((x-1,y))
		else:
			if diag == max(diag, up, left): # case A
					steps.append((x-1,y-1))
			if left == max(diag, up, left): # case B
				steps.append((x,y-1))
			if up == max(diag, up, left):   # case C
				steps.append((x-1,y))
		return steps

#print score('a','a')
	def find_path(self, starter, path=[]):
		path.append(starter)
		#exit clause
		solutions = self.find_further_steps(starter[0], starter[1])
		for solution in solutions:
			if solution == (0,0):
				path.append(solution)
				print 'done', path
				return path
			else:
				further_path = self.find_path(solution, path=path)
				if further_path:
					self.Paths.append(self.find_path(solution, path=path))
			path = path[:path.index(solution)]


for pair in WORDS:
	print 'working on', pair
	A = pair[0]
	B = pair[1]
	matrix= zeros((len(A),len(B)))
	maxScore = 0

	for i in range(1,len(A)):
		for j in range(1,len(B)):
			#print B[j]
			#print score(A[i], B[j])
			seq_score = score(A[i], B[j]) + matrix[i-1][j-1]
			matrix[i][j] = max(seq_score, matrix[i-1][j]+GAP, matrix[i][j-1]+GAP)
			if matrix[i][j] >= maxScore:
				imax = i
				jmax = j
				maxScore = matrix[i][j]
	print matrix

	test = Allignments(matrix, A, B)

	test.find_path((imax, jmax), path=[])
	print test.Paths
	
	#maxindx = matrix.argmax()
	#i = maxindx / matrix.shape[1]
	#j = maxindx % matrix.shape[1]
	#path = []
	#i, j = imax, jmax
	#while i > 0 and j > 0:
		#diag = matrix[i-1][j-1]		
		#up = matrix[i-1][j]		
		#left = matrix[i][j-1]		
		#path.append((i,j))
		#if diag  == max(diag, up, left):
			#i -= 1
			#j -= 1
		#elif up == max(diag, up, left):
			#i -= 1
		#elif left == max(diag, up, left):
			#j -= 1
	#while i > 0:
		#path.append((i,j))
		#i -= 1
	#while j >0:
		#path.append((i,j))
		#j -= 1
	##print imax, jmax
	#print path
