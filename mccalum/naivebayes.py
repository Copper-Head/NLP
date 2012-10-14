#!/sw/bin/python

import math
import sys
import glob
import pickle
from dicts import DefaultDict

# In the documentation and variable names below "class" is the same
# as "category"

def naivebayes (dirs):
    """Train and return a naive Bayes classifier.  
    The datastructure returned is an array of tuples, one tuple per
    class; each tuple contains the class name (same as dir name)
    and the multinomial distribution over words associated with
    the class"""
    classes = []
    for dir in dirs:
	print dir
	countdict = files2countdict(glob.glob(dir+"/*"))
	# Here turn the "countdict" dictionary of word counts into
	# into a dictionary of smoothed word probabilities
	classes.append((dir,countdict))
    return classes

def classify (classes, filename):
    """Given a trained naive Bayes classifier returned by naivebayes(), and
    the filename of a test document, d, return an array of tuples, each
    containing a class label; the array is sorted by log-probability 
    of the class, log p(c|d)"""
    answers = []
    print 'Classifying', filename
    for c in classes:
	score = 0
	for word in open(filename).read().split():
	    word = word.lower()
	    score += math.log(c[1].get(word,1))
	answers.append((score,c[0]))
    answers.sort()
    return answers

def files2countdict (files):
    """Given an array of filenames, return a dictionary with keys
    being the space-separated, lower-cased words, and the values being
    the number of times that word occurred in the files."""
    d = DefaultDict(0)
    for file in files:
	for word in open(file).read().split():
	    d[word.lower()] += 1
    return d
	

if __name__ == '__main__':
    print 'argv', sys.argv
    print "Usage:", sys.argv[0], "classdir1 classdir2 [classdir3...] testfile"
    dirs = sys.argv[1:-1]
    testfile = sys.argv[-1]
    nb = naivebayes (dirs)
    print classify(nb, testfile)
    pickle.dump(nb, open("classifier.pickle",'w'))
