'''
Umass Amherst
Compsci 585 - Introduction to Natural Language Processing.
Instroctor: Andrew McCallum
Submission: Ilia Kurenkov
Assignment 4: Naive Bayes Classifier

This classifier, for testing purposes, uses the nltk movie review corpus.
'''
import datetime
# from operator import mul
from math import log
from collections import defaultdict
from nltk.corpus import movie_reviews as mr 

CLASSES = mr.categories()
TRAINING_POSITIVES1 = mr.fileids(categories='pos')[:500]
TRAINING_NEGATIVES1 = mr.fileids(categories='neg')[:500]

TRAINING_POSITIVES2 = mr.fileids(categories='pos')[:700]
TRAINING_NEGATIVES2 = mr.fileids(categories='neg')[:700]

TRAINING_POSITIVES3 = mr.fileids(categories='pos')[:900]
TRAINING_NEGATIVES3 = mr.fileids(categories='neg')[:900]

TESTING1 = mr.fileids(categories='pos')[500:] + mr.fileids(categories='neg')[500:]
TESTING2 = mr.fileids(categories='pos')[700:] + mr.fileids(categories='neg')[700:]
TESTING3 = mr.fileids(categories='pos')[900:] + mr.fileids(categories='neg')[900:]

################ Training Machinery ########################
'''The way I'm doing this for now may not very good for the memory since it
loads all of the texts together into it.
'''

class Laplace_Label():
	"""this class represents a label. As it is initialized, it processes a 
	collection of filenames the following way:
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
		self.N = len(self.rev) + len(self.V)
		self.word_probs = defaultdict(int, [(w, self.rev.count(w)) for w in self.V])
		
################ Some Testing Machinery #########################

def prob(word, label):
	'''lots of error catching here'''
	if label == 'pos':
		return (pos.word_probs[word]+1.0)/pos.N
	elif label == 'neg':
		return (neg.word_probs[word]+1.0)/neg.N		
	else:
		raise Exception('An invalid label was passed. Exiting...')


def cat_score(review, cat):
	'''gets probability of a document being in a class by summing up
	the log probabilities of the words in the document, given the class.
	'''
	return sum([log(prob(word, cat)) for word in mr.words(review)])


def foo(review):
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
print '''Round 1:\nThe training corpus is 500 reviews for every class\n
The testing corpus is 1000 texts'''
# first we train...
start = datetime.datetime.now()	#start the timer
pos = Laplace_Label(TRAINING_POSITIVES1)		# train positive reviews
print 'size of positive vocabulary: {}'.format(len(pos.V))
neg = Laplace_Label(TRAINING_NEGATIVES1)		# train on negative reviews
print 'size of negative vocabulary: {}'.format(len(neg.V))
finish = datetime.datetime.now()		# stop timer
print 'done training, it took ', finish - start		# print the time it took
# then we test...
start = datetime.datetime.now()			# start timer
classified = [(foo(x), x) for x in TESTING1]		# create list of 
finish = datetime.datetime.now()
print 'done testing, it took ', finish - start
# then we evaluate ...
print 'the F1 value is: {}\n'.format(evaluate(classified, TESTING1))


'''Round 2 with training corpus of 700 for every label. '''
print '''Round 2:\nThe training corpus is 700 reviews for every class\n
The testing corpus is 600 texts'''
# first we train...
start = datetime.datetime.now()	#start the timer
pos = Laplace_Label(TRAINING_POSITIVES2)		# train positive reviews
print 'size of positive vocabulary: {}'.format(len(pos.V))
neg = Laplace_Label(TRAINING_NEGATIVES2)		# train on negative reviews
print 'size of negative vocabulary: {}'.format(len(neg.V))
finish = datetime.datetime.now()		# stop timer
print 'done training, it took ', finish - start		# print the time it took
# then we test...
start = datetime.datetime.now()			# start timer
classified = [(foo(x), x) for x in TESTING2]		# create list of 
finish = datetime.datetime.now()
print 'done testing, it took ', finish - start
# then we evaluate ...
print 'the F1 value is: {}\n'.format(evaluate(classified, TESTING2))


'''Round 3 with training corpus of 700 for every label. '''
print '''Round 3:\nThe training corpus is 900 reviews for every class\n
The testing corpus is 200 texts'''
# first we train...
start = datetime.datetime.now()	#start the timer
pos = Laplace_Label(TRAINING_POSITIVES3)		# train positive reviews
print 'size of positive vocabulary: {}'.format(len(pos.V))
neg = Laplace_Label(TRAINING_NEGATIVES3)		# train on negative reviews
print 'size of negative vocabulary: {}'.format(len(neg.V))
finish = datetime.datetime.now()		# stop timer
print 'done training, it took ', finish - start		# print the time it took
# then we test...
start = datetime.datetime.now()			# start timer
classified = [(foo(x), x) for x in TESTING3]		# create list of 
finish = datetime.datetime.now()
print 'done testing, it took ', finish - start
# then we evaluate ...
print 'the F1 value is: {}\n'.format(evaluate(classified, TESTING3))

''' Sandbox '''

def combine(list1, list2):
	pass