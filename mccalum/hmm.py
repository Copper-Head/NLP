# This code should help get you started, but it is not guaranteed to
# be bug free!  If you find problems, please report to
# compling-class@cs.umass.edu

import sys
from dicts import DefaultDict
from random import choice

def Dict(**args): 
    """Return a dictionary with argument names as the keys, 
    and argument values as the key values"""
    return args

def hmm (file):
    """Given an open FILE, e.g. from the open(filename) function,
    Read pre-tagged sentences of WSJ, one per line.  Return an HMM,
    here represented as a tuple containing (1) the transition probabilities,
    and (2) the emmission probabilities."""
    transitions = DefaultDict(DefaultDict(0))
    emissions = DefaultDict(DefaultDict(0))
    wordcounts = DefaultDict(0)
    # For each sentence (one per line)
    for line in file.xreadlines():
	# for each word in the sentence (space separated)
	prevtag = 'START'   # Before each sentence, begin in START state
	for taggedword in line.split():
	    (word, tag) = taggedword.split('/')
	    transitions[prevtag][tag] += 1
	    emissions[tag][word] += 1
	    wordcounts[word] += 1
    # At test time we will need estimates for "unknown words"---the words
    # the words that never occurred in the training data.  One recommended
    # way to do this is to turn all training words occurring just once 
    # into '<UNKNOWN>' and use this as the stand-in for all "unknown words"
    # at test time.  Below we make all the necessary transformations
    # to '<UNKNOWN>'.
    for tag,dict in emissions.items():
	for word,count in dict.items():
	    if wordcounts[word] == 1:
		del emissions[tag][word]
		emissions[tag]['<UNKNOWN>'] += 1
    # Here you need to add code that will turn these dictionaries 
    # of counts into dictionaries of smoothed conditional probabilities
    return (transitions, emissions)
	    
def viterbi_tags (untagged_sentence):
    """Given a string containing the space-separated words of a sentence;
    (there should even be spaces on either side of punctuation, as in the
    WSJ training data), return an array containing the mostl likely
    sequence of part-of-speech tags."""
    wordarray = untagged_sentence.split()
    # Implement Viterbi here
    # return the mostly likely sequence of part-of-speech tags

def true_tags (tagged_sentence):
    """Given a string containing the space-separated words/POS of a sentence;
    (there should even be spaces on either side of punctuation, as in the
    WSJ training data) pull out and return the tag sequence."""
    wordarray = tagged_sentence.split()
    tags = [word.split('/')[1] for word in wordarray]
    return tags


if __name__ == '__main__':
    print "Usage:", sys.argv[0], "wsjtrainfile wsjtestfile"
    dirs = sys.argv[1:-1]
    testfile = sys.argv[-1]
    h = hmm (sys.stdin)
    print h[0]
    print '------'
    print h[1]
    print true_tags ('The/DT August/NNP deficit/NN and/CC the/DT #/# 2.2/CD billion/CD gap/NN')


