import sys
from random import choice

def Dict(**args): 
    """Return a dictionary with argument names as the keys, 
    and argument values as the key values"""
    return args

# The grammar
# A line like:
#    NP = [['Det', 'N'], ['N'], ['N', 'PP'], 
# means
#    NP -> Det N
#    NP -> N
#    NP -> N PP
grammar = Dict(
        S = [['NP','VP']],
        NP = [['Det', 'N'], ['N', 'PP']],
        VP = [['V', 'NP'], ['V', 'PP']],
	PP = [['P', 'N']],
        Det = ['the', 'a'],
	P = ['with'],
	J = ['red', 'big'],
        N = ['red', 'dog', 'dogs', 'pickles', 'ball', 'light'],
        V = ['pickles', 'see', 'sees', 'liked', 'light', 'slept']
        )

def generate(phrase):
    "Generate a random sentence or phrase"
    if isinstance(phrase, list): 
        return mappend(generate, phrase)
    elif phrase in grammar:
        return generate(choice(grammar[phrase]))
    else: return [phrase]
    
def generate_tree(phrase):
    """Generate a random sentence or phrase,
     with a complete parse tree."""
    if isinstance(phrase, list): 
        return map(generate_tree, phrase)
    elif phrase in grammar:
        return [phrase] + generate_tree(choice(grammar[phrase]))
    else: return [phrase]

def mappend(fn, list):
    "Append the results of calling fn on each element of list."
    return reduce(lambda x,y: x+y, map(fn, list))

def producers(constituent):
    "Argument is a list containing the rhs of some rule; return all possible lhs's"
    results = []
    for (lhs,rhss) in grammar.items():
	for rhs in rhss:
	    if rhs == constituent:
		results.append(lhs)
    return results

def printtable(table, wordlist):
    "Print the dynamic programming table.  The leftmost column is always empty."
    print "    ", wordlist
    for row in table:
	print row

def parse(sentence):
    "The CYK parser.  Return True if sentence is in the grammar; False otherwise"
    global grammar
    # Create the table; index j for rows, i for columns
    length = len(sentence)
    table = [None] * (length)
    for j in range(length):
	table[j] = [None] * (length+1)
	for i in range(length+1):
	    table[j][i] = []
    # Fill the diagonal of the table with the parts-of-speech of the words
    for k in range(1,length+1):
	table[k-1][k].extend(producers(sentence[k-1]))

    #
    # You fill in CYK implementation here
    #

    # Print the table
    printtable(table, sentence)

def printlanguage ():
    "Randomly generate many sentences, saving and printing the unique ones"
    language = {}
    size = 0
    for i in range(100):
	sentencestr = ' '.join(generate('S'))
	language[sentencestr] = 1
	if len(language) > size:
	    size = len(language)
	    print '+',
	else:
	    print '.',
	    sys.stdout.flush()
	print
    for s in language.keys():
	print s
    print size

def printsentence ():
    print ' '.join(generate('S'))


#print producers(['Det', 'N'])
#printsentence()
#parse('the man with the pickles hit the red ball'.split())
printlanguage()
