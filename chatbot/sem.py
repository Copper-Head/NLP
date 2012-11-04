import re

'''
Figuring out what the user is saying
'''

def neg_or_pos(response):
	pos_pts, neg_pts, xpl_pts = 0, 0, 1
	negatives = ['[nN](?:o|ah)t?',
			'[bB]ut',
			'[Ww]rong',
			]
	positives = ['[yY]e(?:s|a)',
			'[aA]bsolutely',
			'[dD]efinitely',
			'[Gg]ood',
			'[Tt]hanks',
			'[Tt]hank [yY]ou',
			'[Rr]ighto?',
			]
	expletives = [ #I don't really know how to deal with them yet 
			'[Ff]uck',
			'[vV]ery',
			]

	pos_pts = len(re.findall('|'.join(positives), response))
	#print pos_pts, re.findall('|'.join(positives), response)
	neg_pts = len(re.findall('|'.join(negatives), response))
	#print neg_pts, re.findall('|'.join(negatives), response)
	xpl_pts += len(re.findall('|'.join(negatives), response))

	score = (pos_pts - neg_pts) * xpl_pts
	
	if score > 2:
		return 'very pos'
	elif 0 < score < 2:
		return 'pos'
	elif -2 < score < 0:
		return 'neg'
	elif score < -2:
		return 'very neg'
	else:
		return 'not sure'

'''testing'''
print neg_or_pos('Yea, but you have the time wrong')


def is_apptmnt_details(response):



