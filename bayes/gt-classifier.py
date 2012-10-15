'''This classifier uses the Good-Turing smoothing. I plan to compare its results
with a classifier that uses Laplace smoothing. I want to compare the performance
of these two algorithms on the movie_review corpus as well as on the spam corpus.
'''

import datetime
from math import log
from collections import defaultdict
from nltk.corpus import movie_reviews as mr

CLASSES = mr.categories()
TRAINING_POSITIVES1 = mr.fileids(categories='pos')[:500]
TRAINING_NEGATIVES1 = mr.fileids(categories='neg')[:500]

TRAINING_POSITIVES2 = mr.fileids(categories='pos')[:700]
TRAINING_NEGATIVES2 = mr.fileids(categories='neg')[:700]

TRAINING_POSITIVES2 = mr.fileids(categories='pos')[:900]
TRAINING_NEGATIVES1 = mr.fileids(categories='neg')[:900]

TESTING1 = mr.fileids(categories='pos')[500:] + mr.fileids(categories='neg')[500:]
TESTING2 = mr.fileids(categories='pos')[700:] + mr.fileids(categories='neg')[700:]
TESTING2 = mr.fileids(categories='pos')[900:] + mr.fileids(categories='neg')[900:]


################ Training Machinery ########################
'''The way I'm doing this for now may not very good for the memory since it
loads all of the texts together into it.
'''

class GT_Label():
	"""this class represents a label. As it is initialized, it processes a 
	collection of filenames the following way:
	REDO REDO REDO REDO
	1. texts corresponding to filenames are extracted and combined into a list
	2. the vocabulary is created from a set of this list
	3. Laplace smooting denominator is calculated
	4. dictionary of word probabilities is created for class.
	"""
	def __init__(self, collection):
		''' constructor takes collection of texts as arg
		'''
		self.rev = [word for text in collection for word in mr.words(text)]
		self.V = set(self.rev)
		self.N = len(self.rev)
		self.word_counts = defaultdict(int, [(w, float(self.rev.count(w))) for w in self.V])
		self.freq_counts = defaultdict(int, {0:self.N})
		for word in self.word_counts: self.freq_counts[self.word_counts[word]] += 100

	def get_prob(self, word):
		k = self.word_counts[word]
		count = (k+1)*self.freq_counts[k+1]/self.freq_counts[k]
		return count/self.N


################ Some Testing Machinery #########################

def prob(word, label):
	'''lots of error catching here
	REDO REDO REDO 
	'''
	if label == 'pos':
		try:
			return pos.word_probs[word]
		except KeyError:
			return 1.0/pos.N
	elif label == 'neg':
		try:
			return neg.word_probs[word]
		except KeyError:
			return 1.0/neg.N
	else:
		raise Exception('An invalid label was passed. Exiting...')


def cat_score(review, cat):
	'''gets probability of a document being in a class by summing up
	the log probabilities of the words in the document, given the class.
	'''
	return -sum([log(prob(word, cat)) for word in mr.words(review)])


def find_class(review):
	'''returns most likely class for a review'''
	return max([(cat_score(review, cat), cat) for cat in CLASSES])[1]


############ Calculating Precision and recall ############

def evaluate(classified, test):
	''' function for evaluating our results. 
	'''
	classified_pos = [x for x in classified if x[0] == 'pos']
	true_positives = [x for x in classified_pos if mr.categories(x[1])[0] == x[0]]
	false_positives = [x for x in classified_pos if mr.categories(x[1])[0] != x[0]]
	precision = 100*float(len(true_positives))/len(classified_pos)
	print 'precision is:', precision
	recall = 100*len(true_positives)/float(len([x for x in test if mr.categories(x)[0]=='pos']))
	print 'recall is', recall

	return 2*precision*recall/(precision+recall)


############### Some Actual testing ##################
''' Round 1, with training corpus of 500 for every label.'''
print '''Trying to figure out where to introduce the quadratic function.'''
# first we train...
start = datetime.datetime.now()	#start the timer
pos = GT_Label(TRAINING_POSITIVES1)		# train positive reviews
print 'finished training, that took:', datetime.datetime.now() - start
print 'size of positive vocabulary: {}\n'.format(len(pos.V))
print pos.freq_counts



''' sandbox '''

'''I need a function that takes in two sequences (corresponding ones)
and generates alpha and beta...
'''

def stdev(values):
	'''This method computes the sample standard deviation for a given list
	of values. Its accuracy has been compared to that of wolfram alpha and 
	has been shown to be on par. Taken from data_analyzer.py
	'''
	n = len(values)
	mean = float(sum(values))/n
	return sqrt(sum([pow(v-mean,2) for v in values])/(n-1))

def reg_average(collection):
	'''taken from average.py, this function returns sample average
	for a given list. '''
	return float(sum(collection))/len(collection)

def linear(X,Y):
	n = len(X)
	r = sum([x*y-reg_average(Y)*reg_average(X) for x in X for y in Y])/(n-1.0)*stdev(X)*stdev(Y)
	beta = r*stdev(X)/stdev(Y)
	alpha = reg_average(Y) - beta*reg_average(X)