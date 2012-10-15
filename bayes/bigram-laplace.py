'''
Umass Amherst
Compsci 585 - Introduction to Natural Language Processing.
Instroctor: Andrew McCallum
Submission: Ilia Kurenkov
Assignment 4: Naive Bayes Classifier

This classifier, for testing purposes, uses the nltk movie review corpus.
This version is practically identical to the trigram one, but uses bigrams
due to the fact that bigrams seem to unanimously favor negative reviews.
'''
import re
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

	"""
	def __init__(self, collection):
		''' constructor takes collection of texts as arg
		'''
		(self.bigrams, self.N) = self.add_bigrams([word for text in collection 
			for word in mr.words(text)])
		self.unigrams = self.add_unigrams([word for text in collection 
			for word in mr.words(text)])
		

	def add_bigrams(self, text):
		bigrams = defaultdict(int)
		count = 0.0
		for i in range(len(text)-1):
			bigrams[' '.join([text[i], text[i+1],])] += 1
			count += 1.0
		return (bigrams, len(bigrams))

	def add_unigrams(self, text):
		unigrams = defaultdict(int)
		for i in range(len(text)-1):
			unigrams[' '.join([text[i], text[i+1],])] += 1
		return unigrams

		
################ Some Testing Machinery #########################

def prob(word, next_word, label):
	'''lots of error catching here'''
	if label == 'pos':
		return (pos.bigrams[word + ' '+ next_word]+1.0)/(pos.unigrams[word]+pos.N)
	elif label == 'neg':
		return (neg.bigrams[word + ' '+ next_word]+1.0)/(neg.unigrams[word]+neg.N)
	else:
		raise Exception('An invalid label was passed. Exiting...')


def cat_score(review, cat):
	'''gets probability of a document being in a class by summing up
	the log probabilities of the words in the document, given the class.
	'''
	text = mr.words(review)
	return sum([log(prob(text[i],text[i+1], cat)) for i in range(len(text)-1)])


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
	print 'portion of overall correct', 100.0*len([x for x in classified 
		if x[0] == mr.categories(x[1])[0]])/len(test)

	return 2*precision*recall/(precision+recall)


############### Some Actual testing ##################
''' Round 1, with training corpus of 500 for every label.'''
print '#'*80
print '''Round 1 with bigrams:\nThe training corpus is 500 reviews for every class\n
The testing corpus is 1000 texts'''
# first we train...
start = datetime.datetime.now()	#start the timer
pos = Laplace_Label(TRAINING_POSITIVES1)		# train positive reviews
print 'size of positive vocabulary: {}'.format(len(pos.bigrams))
# print pos.bigrams
neg = Laplace_Label(TRAINING_NEGATIVES1)		# train on negative reviews
print 'size of negative vocabulary: {}'.format(len(neg.bigrams))
finish = datetime.datetime.now()		# stop timer
print 'done training, it took ', finish - start		# print the time it took
# then we test...
start = datetime.datetime.now()			# start timer
classified = [(find_class(x), x) for x in TESTING1]		# create list of
# print classified
finish = datetime.datetime.now()
print 'done testing, it took ', finish - start
# then we evaluate ...
print 'the F1 value is: {}\n'.format(evaluate(classified, TESTING1))


'''Round 2 with training corpus of 700 for every label. '''
print '''Round 2 with bigrams:\nThe training corpus is 700 reviews for every class\n
The testing corpus is 600 texts'''
# first we train...
start = datetime.datetime.now()	#start the timer
pos = Laplace_Label(TRAINING_POSITIVES2)		# train positive reviews
print 'size of positive vocabulary: {}'.format(len(pos.bigrams))
neg = Laplace_Label(TRAINING_NEGATIVES2)		# train on negative reviews
print 'size of negative vocabulary: {}'.format(len(neg.bigrams))
finish = datetime.datetime.now()		# stop timer
print 'done training, it took ', finish - start		# print the time it took
# then we test...
start = datetime.datetime.now()			# start timer
classified = [(find_class(x), x) for x in TESTING2]		# create list of 
finish = datetime.datetime.now()
print 'done testing, it took ', finish - start
# then we evaluate ...
print 'the F1 value is: {}\n'.format(evaluate(classified, TESTING2))


'''Round 3 with training corpus of 700 for every label. '''
print '''Round 3 with bigrams:\nThe training corpus is 900 reviews for every class\n
The testing corpus is 200 texts'''
# first we train...
start = datetime.datetime.now()	#start the timer
pos = Laplace_Label(TRAINING_POSITIVES3)		# train positive reviews
print 'size of positive vocabulary: {}'.format(len(pos.bigrams))
neg = Laplace_Label(TRAINING_NEGATIVES3)		# train on negative reviews
print 'size of negative vocabulary: {}'.format(len(neg.bigrams))
finish = datetime.datetime.now()		# stop timer
print 'done training, it took ', finish - start		# print the time it took
# then we test...
start = datetime.datetime.now()			# start timer
classified = [(find_class(x), x) for x in TESTING3]		# create list of 
finish = datetime.datetime.now()
print 'done testing, it took ', finish - start
# then we evaluate ...
print 'the F1 value is: {}\n'.format(evaluate(classified, TESTING3))

