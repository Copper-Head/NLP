'''
Compsci 585
Instructor: Andrew McCallum
Assignment #4
by: Ilia Kurenkov


In this submission I decided to compare the performance of the Kneser-Ney 
smoothing algorithm to that of Laplace smoothing. See my report for more 
details on the reasoning behind this and the sources I used.
'''
import time					# just to keep track of how long things run
from math import log 		# convert probs to logs to prevent underflow
from collections import defaultdict
from nltk.corpus import movie_reviews as mr
###############################################################################
############################## OUR MODELS #####################################
###############################################################################
class Laplace_Ugram_Label():
	"""
	A Laplace Unigram label. 
	In my program this class is used as a base for all other classes.
	"""
	def __init__(self, collection, tag):
		'''
		Class constructor.
		@type	tag :: string
		@param 	tag :: name of tag 
		@type	collection :: list of strings
		@param 	collection :: list of file names
		'''
		self.tag = tag
		self.rev = [word for text in collection for word in mr.words(text)]
		self.unigrams = defaultdict(int)
		for w in self.rev: self.unigrams[w] += 1
		self.N = len(self.rev) + len(self.unigrams)

	''' methods for getting probabilities '''
	def prob(self, word):
		'''
		Returns the probability of word for this class.
		'''
		return (self.unigrams[word]+1.0) / self.N

	def review_score(self, review):
		'''
		Gets the probability score for a given review.
		'''
		return sum(log(self.prob(word)) for word in mr.words(review))

class Laplace_Bgram_Label(Laplace_Ugram_Label):
	"""
	Laplace Bigram class. Extends the Unigram class, adds onto it counting of 
	bigrams.
	"""
	def __init__(self, collection, tag):
		''' 
		Constructor. Calls on the constructosuper(Pees, self).__init__()
		self.arg = argr for the Unigram class, then
		counts the bigrams.
		'''
		Laplace_Ugram_Label.__init__(self, collection, tag)
		self.bigrams = defaultdict(int)
		for i in range(len(self.rev)-1):
			self.bigrams[(self.rev[i],self.rev[i+1])] += 1
		self.N = len(self.rev) + len(self.bigrams)

	''' methods for getting probabilities '''
	def prob(self, bigram):
		'''
		Return the probability of bigram.
		'''
		return (self.bigrams[bigram]+1.0)/(self.unigrams[bigram[0]]+self.N)

	def review_score(self, review):
		'''
		Extract the words from file name and return the probability score 
		for this label for this review.
		'''
		text = mr.words(review)
		return sum(self.prob((text[i], text[i+1])) for i in range(len(text)-1))

class Laplace_Tgram_Label(Laplace_Bgram_Label):
	"""
	Trigram Laplace Label. Extends the Bigram label class. 
	In addition counts the trigrams. 
	"""
	def __init__(self, collection, tag):
		''' 
		Constructor. Calls on the bigram constructor.
		In addition, counts trigram frequencies.
		'''
		Laplace_Bgram_Label.__init__(self, collection, tag)
		self.trigrams = defaultdict(int)
		for i in range(len(self.rev)-2):
			self.trigrams[(self.rev[i],self.rev[i+1], self.rev[i+2])] += 1
		self.N = len(self.trigrams)
	
	''' 
	Methods for getting probabilities.
	'''
	def prob(self, trigram):
		'''
		Return the probability of a given a trigram.
		'''
		return (self.trigrams[trigram]+1.0)/(self.bigrams[trigram[:2]]+self.N)

	def review_score(self, review):
		'''
		Given a review return the probability of the label given this review.
		'''
		text = mr.words(review)
		return sum(self.prob((text[i], text[i+1], text[i+2])) 
			for i in range(len(text)-2))

class KN_Label(Laplace_Bgram_Label):
	"""
	Class for the modified Kneser-Ney smoothing. Extends the Laplace Bigram
	class, with the exception of reworking slightly the way probabilities are 
	calculated.
	"""
	def __init__(self, collection, tag):
		''' constructor takes collection of texts as arg and does the following:
		1. runs the Laplace Bigram constructor
		2. calculates the discount values
		3. creates gamma values for all seen words
		4 . creates bigram probabilities for seen words

		Note: the class defaultdict is used throughout this program to account
		for zero count/probability being assigned to completely novel ngrams.
		'''
		Laplace_Bgram_Label.__init__(self, collection, tag)

		self.D = {0:0.0}
		self.calculate_discounts()
		
		self.word_gammas = defaultdict(lambda: {1:0, 2:0, 3:0})
		for bg in self.bigrams.keys():
			bg_cnt = self.bigrams[bg]
			if bg_cnt >= 3:
				self.word_gammas[bg[0]][3] += 1
			else:
				self.word_gammas[bg[0]][bg_cnt] += 1
		
		self.bigram_probs = defaultdict(float)
		for bg in self.bigrams.keys():
			self.bigram_probs[bg] = self._prob(bg)

	def calculate_discounts(self):
		'''
		Once we collect all the counts we need to estimate the discounts' 
		values. This method is basically an addendum to the constructor.
		'''
		NN = dict([(y,sum(1.0 for x in self.bigrams if self.bigrams[x] == y))
			for y in range(1,5)])
		BigY = float(NN[1]) / (NN[1] + 2*NN[2])
		for i in range(1,4):
			self.D[i] = i - (i+1)*BigY*NN[i+1] / NN[i]

###############################################################################
	def kn_count(self, bigram):
		'''
		Returns absolute discounted count of a bigram over the number of bigrams
		containing the first member (the same as its count).
		'''
		count = self.bigrams[bigram]
		if self.D.has_key(count):
			discount = self.D[count]
		else:
			'''this is if the count is higher than 3'''
			discount = self.D[3]

		denominator = self.unigrams[bigram[0]]
		if denominator:
			'in case the first member of bigram does occur in training'
			return (count - discount) / denominator
		else:
			'in case the first member of the bigram never occurs in training'
			return 0.0

###############################################################################
	def gamma(self, word):
		'''
		Given a word returns the gamma of it in accordance with the formula
		from page 20 or the Chen-Goodman 1995 paper.
		The numerator consists of all discounts multiplied by correspoding 
		counts of bigrams. The denominator is the number of bigrams where word 
		is the first member.
		'''
		denominator = self.unigrams[word]
		if denominator:
			'if the word occurs in training'
			prev_context = self.word_gammas[word]
			numerator = sum(self.D[i]*prev_context[i] for i in range(1,4))
			return float(numerator) / denominator
		else:
			return 0.0

###############################################################################
	def _prob(self,ngram):
		'''internal probability calculator'''
		ugram_prob = float(self.unigrams[ngram[1]]) / len(self.bigrams)
		bgram_prob = float(self.bigrams[ngram]) / self.unigrams[ngram[0]]
		prob = bgram_prob + self.gamma(ngram[0])*ugram_prob
		# print prob, ngram
		return log(prob)

	def prob(self, bigram):
		bigram_prob = self.bigram_probs[bigram]
		if bigram_prob:
			return bigram_prob
		else:
			ugram_prob = float(self.unigrams[bigram[1]]) / len(self.bigrams)
			return self.gamma(bigram[1]) * ugram_prob
	
	def review_score(self, review):
		'''
		take in a review, return a score for this given label.
		'''
		text = mr.words(review)
		return sum(self.prob((text[i], text[i+1]))
			for i in range(len(text)-1))

###############################################################################
######################### Some Testing Machinery ##############################
###############################################################################
def find_class(review_name, category_list):
	'''
	Takes a review_name and returns the most likely corresponding class.
	'''
	return max((cat.review_score(review_name), cat.tag) for cat in category_list)[1]

def test_model(test_data, category_list):
	'''
	This method presupposes a collection of filenames as test_data.
	Returns a list of tuples (class, file_name).
	'''
	return [(find_class(x, category_list), x) for x in test_data]

def evaluate(test, category_list):
	'''
	Function returns number of reviews the tags of which we predicted correctly. 
	'''
	return 100.0*sum(1 for x in test_model(test, category_list) 
		if x[0] == mr.categories(x[1])[0])/len(test)

def average(collection):
	'''
	This function returns sample average for a given list of numbers. 
	Make sure not to pass this function any strings!!
	'''
	try:
		return float(sum(collection))/len(collection)
	except ZeroDivisionError:
		print "For some reason got an empty list"
		return 0.0

###############################################################################
########################### RUNNING THE CORPORA ###############################
###############################################################################
''' 
We start by defining a bunch of lists to store our running statistics for every
model: the accuracy, the training and testing times. 
These values will later be used to calculate the average.
'''

laplace_u_score = []
laplace_u_train_time = []
laplace_u_test_time = []

laplace_b_score = []
laplace_b_train_time = []
laplace_b_test_time = []

laplace_t_score = []
laplace_t_train_time = []
laplace_t_test_time = []

kn_score = []
kn_train_time = []
kn_test_time = []

''' 
The cross-verifying part. We take a segment of 100 texts from both the positive
and the negative corpora and use it for testing. The remaining total 1800 texts
would be used for training. 10 passes were made over the data, each time a
different segment of it was set aside as testing data.
'''
for i in range(0,900, 100):
	print 'Starting loop ', i
	all_pos = mr.fileids(categories='pos')
	all_neg = mr.fileids(categories='neg')
	testing_texts = set(all_pos[i:i+100] + all_pos[i:i+100])

	training_pos = set(all_pos) - testing_texts
	training_neg = set(all_neg) - testing_texts

	start = time.time()
	laplace_u_models = [Laplace_Ugram_Label(training_pos, 'pos'), 
		Laplace_Ugram_Label(training_neg, 'neg')]
	traintime = time.time()
	print 'done training Laplace Unigrams...'
	laplace_u_score.append(evaluate(testing_texts, laplace_u_models))
	laplace_u_test_time.append(time.time() - traintime)
	laplace_u_train_time.append(traintime - start)
	print 'done testing Laplace Unigrams...'

	start = time.time()
	laplace_b_models = [Laplace_Bgram_Label(training_pos, 'pos'), 
		Laplace_Bgram_Label(training_neg, 'neg')]
	traintime = time.time()
	print 'done training Laplace Bigrams...'
	laplace_b_score.append(evaluate(testing_texts, laplace_b_models))
	laplace_b_test_time.append(time.time() - traintime)
	laplace_b_train_time.append(traintime - start)
	print 'done testing Laplace Bigrams...'

	start = time.time()
	laplace_t_models = [Laplace_Tgram_Label(training_pos, 'pos'), 
		Laplace_Tgram_Label(training_neg, 'neg')]
	traintime = time.time()
	print 'done training Laplace Trigrams...'
	laplace_t_score.append(evaluate(testing_texts, laplace_t_models))
	laplace_t_test_time.append(time.time() - traintime)
	laplace_t_train_time.append(traintime - start)
	print 'done testing Laplace Trigrams...'

	start = time.time()
	kn_models = [KN_Label(training_pos, 'pos'), KN_Label(training_neg, 'neg')]
	traintime = time.time()
	print 'done training KN, took', traintime - start
	kn_score.append(evaluate(testing_texts, kn_models))

	kn_test_time.append(time.time() - traintime)
	kn_train_time.append(traintime - start)
	print 'done testing KN'

'''
Now we write our results to a file.
'''
with open('first-testing.txt', 'w') as f:
	stuff_to_write = {'Laplace Unigrams': [laplace_u_score,
											laplace_u_train_time,
											laplace_u_test_time],
						'Laplace Bigrams': [laplace_b_score,
											laplace_b_train_time,
											laplace_b_test_time],
						'Laplace Trigrams': [laplace_t_score,
											laplace_t_train_time,
											laplace_t_test_time],
						'Kneser-Ney': [kn_score,
										kn_train_time,
										kn_test_time],
						}
	f.write('Comparing the performance of unigrams Laplace with Kneser-Ney')
	for x in stuff_to_write.keys():
		f.write('''\n Below are the results for {0}: \n
The average accuracy across 10 iterations was: \n{1}\n
The average training time across 10 iterations was: \n{2}\n
The average testing time across 10 iterations was: 
\n{3}\n'''.format(x, average(stuff_to_write[x][0]),	
	average(stuff_to_write[x][1]), average(stuff_to_write[x][2])))