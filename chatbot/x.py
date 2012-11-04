import re
import time
from random import randint
#from datetime import date

'''
Some issues: we will need to somehow perfect the regex that catches dates so
that it doesn't process phrases like "forty fifth" or "fifty first".
We will also need to consider how times are given and add some functionality
with regards to catching them
'''

############ Mappings #########################
months = {
		'January': ('[jJ]anuary', 1),
		'February': ('[Ff]ebruary', 2),
		'March': ('[Mm]arch', 3),
		'April': ('[Aa]pril', 4),
		'May': ('[Mm]ay', 5),
		'June': ('[Jj]une', 6),
		'July': ('[Jj]uly', 7),
		'August': ('[Aa]ugust', 8),
		'September': ('[Ss]eptember', 9),
		'October': ('[Oo]cotober', 10),
		'November': ('[Nn]ovember', 11),
		'December': ('[Dd]ecember', 12),
		}

dates = {
		1 : '(?:\D|^)1(?:st)?|(?<!twenty|thirty) [fF]irst',
		2: '(?:\D|^)2(?:nd)?|(?<!twenty|thirty) [Ss]econd',
		3 : '(?:\D|^)3(?:rd)?|(?<!twenty|thirty) [tT]hird',
		4 : '(?:\D|^)4(?:th)?|(?<!twenty|thirty) [fF]ourth',
		5 : '(?:D|^)5(?:th)?|(?<!twenty|thirty) [Ff]ifth',
		6 : '(?:D|^)6(?:th)?|(?<!twenty|thirty) [sS]ixth',
		7 : '(?:D|^)7(?:th)?|(?<!twenty|thirty) [sS]eventh',
		8 : '(?:D|^)8(?:th)?|(?<!twenty|thirty) [eE]ighth',
		9 : '(?:D|^)9(?:th)?|(?<!twenty|thirty) [nN]inth',
		10 : '(?:D|^)10(?:th)?|[tT]enth',
		11 : '(?:D|^)11(?:th)?|[eE]leventh',
		12 : '(?:D|^)12(?:th)?|[tT]welfth',
		13 : '(?:D|^)13(?:th)?|[tT]hirteenth',
		14 : '(?:D|^)14(?:th)?|[fF]ourteenth',
		15 : '(?:D|^)15(?:th)?|[fF]ifteenth',
		16 : '(?:D|^)16(?:th)?|[sS]ixteenth',
		17 : '(?:D|^)17(?:th)?|[sS]eventeenth',
		18 : '(?:D|^)18(?:th)?|[eE]ighteenth',
		19 : '(?:D|^)19(?:th)?|[nN]ineteenth',
		20 : '(?:D|^)20(?:th)?|[tT]wentieth',
		21 : '(?:D|^)21(?:st)?|[tT]wenty [fF]irst',
		22 : '(?:D|^)22(?:nd)?|[tT]wenty [sS]econd',
		23 : '(?:D|^)23(?:rd)?|[tT]wenty [Tt]hird',
		24 : '(?:D|^)24(?:th)?|[tT]went [fF]ourth',
		25 : '(?:D|^)25(?:th)?|[tT]wenty [fF]ifth',
		26 : '(?:D|^)26(?:th)?|[tT]wenty [sS]ixth',
		27 : '(?:D|^)27(?:th)?|[tT]wenty [sS]eventh',
		28 : '(?:D|^)28(?:th)?|[tT]wenty [eE]ight',
		29 : '(?:D|^)29(?:th)?|[tT]wenty [nN]inth',
		30 : '(?:D|^)30(?:th)?|[tT]hirtieth',
		31 : '(?:D|^)31(?:th)?|[tT]hirty [fF]irst',
		}

days = {
		'Monday' : ('[mM]onday', 0),
		'Tuesday' : ('[Tt]uesday', 1),
		'Wednesday' : ('[Ww]ednesday', 2),
		'Thursday': ('[Tt]hursday', 3),
		'Friday' : ('[Ff]riday', 4),
		'Saturday' : ('[sS]aturday', 5),
		'Sunday': ('[Ss]unday', 6),
		}

hours = {
		1: 'one am',
		2: 'two am',
		3: 'three am',
		4: 'four am',
		5: 'five am',
		6: 'six am',
		7: 'seven am',
		8: 'eight am',
		9: 'nine am',
		10: 'ten am',
		11: 'eleven am',
		12: 'twelve pm',
		13: 'one pm',
		14: 'two pm',
		15: 'three pm',
		16: 'four pm',
		17: 'five pm',
		18: 'six pm',
		19: 'seven pm',
		20: 'eight pm',
		21: 'nine pm',
		22: 'ten pm',
		23: 'eleven pm',
		24: 'twelve pm',
		}
data = [months, days, hours]


''' Misc responses predefined'''
no_comprendo = [
		"I'm not entirely sure I know what {} you mean.",
		"I don't think I got that {}.",
		]
ask_again = [
		'Can you tell me that again, please?',
		'Could you repeat that for me one more time?',
		]

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

class Event:
	def __init__(self):
		self.month = None
		self.day = None
		self.date = None
		self.hour = None
	
	def is_complete(self):
		'''check if all of the data has been collected '''
		#if self.month and self.day and self.date and self.hour:
		if self.month and self.day:
			return True
		else:
			return False
	
	def is_empty(self):
		'''check if no data has been collected '''
		#if not self.month and not self.day and not self.date and not self.hour:
		if not self.month and not self.day:
			return True
		else:
			return False
	
	def get_details(self, inpt):
		'''I have deliberately limited myself to finding out the month and the
		day only, just so that I could figure out how to set up the algorithm
		for that.
		Essentially, the same procedure can be applied to dates and to hours, one
		would just want to keep track of any additional caveats these datatypes
		will present.
		You might, for example, add support for minutes or fine-tune the
		regular expressions involved with either one of the formats
		'''

		month_candidates = []
		day_candidates = []
		#date_candidates = []
		#hour_candidates = []

		''' first round of setting the details. Here we just go over the user's
		response and see if we can pick up on any date info whatsoever. If it
		is the case that we got everything, we simply proceed further. If the
		opposite is true, we check with the user if they want to proceed. If we
		manage to get only part of the information, we reask the user about the
		uncollected pieces until we get the right input.
		'''
		for m in months:
			month_candidates += re.findall(months[m][0], inpt)

		if len(month_candidates) == 1:
			current_event.month = month_candidates[0]

		for d in days:
			day_candidates += re.findall(days[d][0], inpt)

		if len(day_candidates) == 1:
			current_event.day = day_candidates[0]
		
		# this is in case nothing doesn't get collected
		if self.is_empty():
			inpt = raw_input('Are you sure you want to set a date today?')
			if 'neg' in neg_or_pos(inpt):
				''' I am using "break" in this case, but by that I simply mean
				exit the program. I thought it would be easier for you to
				recode if I just had one silly line of code and lots of
				comments than the other way around.
				'''
				break
		
		''' this is in case something doesn't get collected. We essentially
		guide/force the user to give us a month and a day that make sense. We
		do so keeping "in mind" all of the entries we already collected, so the
			user doesn't have to reenter stuff for things that they already
			entered.
			'''
		while not self.is_complete():
			# finding a month
			while not self.month:
				for m in months:
					month_candidates += re.findall(months[m][0], inpt)

				# if all goes well
				if len(month_candidates) == 1:
					current_event.month = month_candidates[0]
					#break
				
				# if we pick up more than one month name 
				elif len(month_candidates) > 1:
					a = randint(0, len(no_comprendo)-1)
					b = randint(0, len(ask_again) - 1)
					inpt = raw_input('\n'.join([no_comprendo[a].format('month'),
								ask_again[b], '']))

				# if we do not find any month names
				elif len(month_candidates) < 1:
					a = randint(0, len(no_comprendo)-1)
					b = randint(0, len(ask_again) - 1)
					inpt = raw_input('\n'.join([no_comprendo[a].format('month'),
								ask_again[b], '']))

			# finding day
			while not self.day:
				for d in days:
					day_candidates += re.findall(days[d][0], inpt)

				if len(day_candidates) == 1:
					current_event.day = day_candidates[0]
				
				# if we pick up more than one day name 
				elif len(day_candidates) > 1:
					a = randint(0, len(no_comprendo)-1)
					b = randint(0, len(ask_again) - 1)
					inpt = raw_input('\n'.join([no_comprendo[a].format('day'),
								ask_again[b], '']))
				
				# if we do not find any day names
				elif len(day_candidates) < 1:
					a = randint(0, len(no_comprendo)-1)
					b = randint(0, len(ask_again) - 1)
					inpt = raw_input('\n'.join([no_comprendo[a].format('day'),
								ask_again[b], '']))

## finding the date
			#for d in dates:
				#date_candidates += re.findall(dates[d], inpt)

			#if len(date_candidates) == 1:
				#current_event.date = date_candidates[0]
			#elif len(date_candidates) > 1:
				#print 'Did you mean {}?'.format(' or '.join(date_candidates))

		else:
			self.display()


	def display(self):
		'''just for development purposes, can be rewritten later to do
		something more prodictive.
		'''
		print self.month, self.day, self.date, self.hour
	
	def make_today(self):
		'''some future functionality for setting the date to the day of the
		conversation. This is unused for now, but I would like to have to be
		able to use the current date as a reference point in the future for
		parsing stuff like "next week" or "tomorrow" or "in a month"
		'''
		p = '(\w{3}) (\w{3}) (.{1,2}) (.{2}):'
		today = re.match(p, time.ctime()).groups()
		self.month = today[0]
		self.day = today[1]
		self.date = today[2]
		self.hour = today[3]
	

'''The below section was just a simple way to test the program's logic without
using the IRC library. '''

inpt = raw_input('Hi, what appointment would you like to set up? \n')

current_event = Event()
current_event.get_details(inpt)

