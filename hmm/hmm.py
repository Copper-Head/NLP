# This code should help get you started, but it is not guaranteed to
# be bug free!  If you find problems, please report to
# compling-class@cs.umass.edu

import sys
# from dicts import DefaultDict
from collections import defaultdict
from random import choice
from math import log

def Dict(**args): 
    """Return a dictionary with argument names as the keys, 
    and argument values as the key values"""
    return args

class hmm():
    """I found that turning the hmm() function into a class was more convenient
    for running the viterbi_tags() function later on.
    """
    def __init__(self, fyle):
        """Given an open FILE, e.g. from the open(filename) function,
        Read pre-tagged sentences of WSJ, one per line. 
        Construct an HMM with three dictionaries:
        - transition probabilities
        - emission probabilities
        - counts of individual words

        We start by initializing them as defaultdicts.
        """
        self.transitions = defaultdict(lambda: defaultdict(float))
        self.emissions = defaultdict(lambda: defaultdict(float))
        self.wordcounts = defaultdict(float, {'<UNKNOWN>':0.0})

        # For each sentence (input file should have one per line)
        for line in fyle.xreadlines():
            # for each word in the sentence (space separated)
            prevtag = 'START'   # Before each sentence, begin in START state
            # split the sentence into words and their tags
            tagged_words = ((word.replace('\/','\\').split('/')) 
                for word in line.split())
            # loop over words and tags incrementing the counts in our dicts
            for word, tag in tagged_words:
                self.transitions[prevtag][tag] += 1.0
                self.emissions[tag][word] += 1.0
                self.wordcounts[word] += 1.0
                # reset the previous tag to the current one
                prevtag = tag
        # At test time we will need estimates for "unknown words"---the words
        # the words that never occurred in the training data.  One recommended
        # way to do this is to turn all training words occurring just once 
        # into '<UNKNOWN>' and use this as the stand-in for all "unknown words"
        # at test time.  Below we make all the necessary transformations
        # to '<UNKNOWN>'.
        for tag, dictionary in self.emissions.items():
            for word in dictionary.keys():
                if self.wordcounts[word] == 1:
                    del dictionary[word]
                    del self.wordcounts[word]
                    self.emissions[tag]['<UNKNOWN>'] += 1
        # now that we are done with all the counts we calculate the probs
        # first the transition probabilities
        for tag, continuations in self.transitions.items():
            #for brevity and efficiency, we calc the denominator first
            denom = sum(len(self.transitions),
            sum(val for val in continuations.values()))
                for nexttag in self.transitions.keys():
                self.transitions[tag][nexttag] = log((continuations[nexttag]+1)/denom)
        #then the emission probabilities
        for tag, words in self.emissions.items():
            #for brevity and efficiency, we calc the denominator first
            denom = sum(len(self.wordcounts),
            sum(val for val in words.values()))
                for word in self.wordcounts.keys():
                self.emissions[tag][word] = log((words[word]+1)/denom)

    def viterbi_tags(self, untg):
        """
        Given an untagged list of words as strings and an hmm returns sequence
        of tags determined by Viterbi.
        """
        untg.reverse()      #Viterbi starts at the end of the sentence
        #if the word was not seen at all during training treat is as "Unknown"
        if not self.wordcounts.has_key(untg[0]):
            untg[0] = '<UNKNOWN>'
        if len(untg) == 1:
            ''' If we have reached the first word of the sequence'''       
            return [(trans_prob + self.emissions[s][untg[0]], [s]) 
                    for s, trans_prob in self.transitions['START'].items()
                    if s!='START']
        
        else:
            '''If not at end of the input list, run 
            '''
            prev_step = self.viterbi_tags(untg[1:])
            return [max((self.transitions[oldstate[-1]][state] + 
                    self.emissions[state][untg[0]] + 
                    score, oldstate + [state]) 
                    for score, oldstate in prev_step)
                    for state in self.transitions.keys() if state!='START']

def true_tags(tagged_sentence):
    """Given a string containing the space-separated words/POS of a sentence;
    (there should even be spaces on either side of punctuation, as in the
    WSJ training data) pull out and return the tag sequence."""
    wordarray = tagged_sentence.split()
    tags = [word.split('/')[1] for word in wordarray]
    return tags

def compare_tags(seq1, seq2):
    '''Function assumes len(seq1) equals len(seq2).
    I used it in testing to compare the results of my viterbi_tags() with those
    of true_tags()'''
    return sum(int(seq1[i]==seq2[i]) for i in range(len(seq1)))

if __name__ == '__main__':
    print "Usage:", sys.argv[0], "wsjtrainfile wsjtestfile"
    h = hmm(sys.stdin)      # here we train the HMM on first passed filename
    testfile = sys.argv[-1]     # testfile is last passed filename

    '''Now for some testing.'''
    with open(testfile, 'r') as fyle:
        correct = 0         # number of correct tags
        total = 0           # total number of processe tags
        for line in fyle:   # loop over lines in file
            # make line processable by viterbi_tages()
            line_norm = [x.split('/')[0] for x in line.split()]
            # compare viterbi tags to true ones, get number correct
            correct += compare_tags(true_tags(line), 
                        max(h.viterbi_tags(line_norm))[1])
            total += len(line_norm)     # add number of words processed
        print correct, total, 100.0*correct/total


