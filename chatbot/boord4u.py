#!/usr/bin/python
		
import re
from random import randint

DEBUG = True

prags = {
	# current-state: {
	#	['output1', 'output2', ...]
	#	{
	#		input-type: next-state,
	#		input-type: (next-state-if-true, next-state-if-false),
	#	}
	# }
	# or don't wait for user input:
	# current-state: next-state

	'greeting': (
		['Hello!'],
		{
			'greeting': 'want-appointment-p',
			'request': 'appointment-make'
		}
	),
	'want-appointment-p': (
		['Would you like to make an appointment?'],
		{
			'boolean': ('appointment-make', 'exit'),
			'appointment': 'confirm-appointment',
			'appointment-incomplete': 'appointment-supplement'
		}
	),
	'appointment-make': (
		['When would you like this appointment?'],
		{
			'appointment': 'confirm-appointment', 'appointment-incomplete': 'appointment-supplement'} ),
	'appointment-supplement': (
		['Could you give me more information about the appointment, currently all I know is {}.'],
		{
			'appointment': 'confirm-appointment',
			'appointment-incomplete': 'appointment-supplement'
		}
	),
	'appointment-correct': (
		['Can you tell me that appointment again, please?', 'Could you repeat that appointment for me one more time?'],
		{
			'appointment': 'confirm-appointment',
			'appointment-incomplete': 'appointment-supplement'
		}
	),
	'confirm-appointment': (
		['Is this appointment correct?: {}'],
		{
			'boolean': ('exit', 'appointment-correct'),
			'appointment': 'confirm-appointment',
			'appointment-incomplete': 'appointment-supplement'
		}
	),
	'make-another': (
		['Would you like to make another appointment?'],
		'want-appointment-p'
	),
	'exit': (
		['Thank you, come again!'],
		{}
	)
}

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
	'October': ('[Oo]ctober', 10),
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

def pos_or_neg(response):
	pos_pts, neg_pts, xpl_pts = 0, 0, 1
	negatives = [
		'[nN](?:o|ah)t?',
		'[bB]ut',
		'[Ww]rong',
	]
	positives = [
		'[yY]e(?:s|a)',
		'[aA]bsolutely',
		'[dD]efinitely',
		'[Gg]ood',
		'[Tt]hanks',
		'[Tt]hank [yY]ou',
		'[Rr]ighto?',
		'[sS]ure',
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

	return (pos_pts - neg_pts) * xpl_pts

class Event:
	def __init__(self):
		self.month = None
		self.day = None
		self.date = None
		self.hour = None
	
	def is_complete(self):
		'''check if all of the data has been collected '''
		#if self.month and self.day and self.date and self.hour:
		if self.month and self.day and self.hour:
			return True
		else:
			return False
	
	def is_empty(self):
		'''check if no data has been collected '''
		#if not self.month and not self.day and not self.date and not self.hour:
		if not self.month and not self.day and not self.hour:
			return True
		else:
			return False

	def details(self, i):
		month_candidates = []
		day_candidates = []
		#date_candidates = []
		hour_candidates = []

		for m in months:
			month_candidates += re.findall(months[m][0], i)

		if len(month_candidates) == 1:
			self.month = month_candidates[0]

		for d in days:
			day_candidates += re.findall(days[d][0], i)

		if len(day_candidates) == 1:
			self.day = day_candidates[0]
		
		"""for d in dates:
			date_candidates += re.findall(dates[d][0], i)

		if len(date_candidates) == 1:
			self.date = date_candidates[0]"""
		
		for h in hours:
			hour_candidates += re.findall(hours[h], i)

		if len(hour_candidates) == 1:
			self.hour = hour_candidates[0]
	
	def interrogate(self, inpt):
		no_comprendo = [
			"I'm not entirely sure I know what {} you mean.",
			"I don't think I got that {}.",
		]
		ask_again = [
			'Can you tell me that again, please?',
			'Could you repeat that for me one more time?',
		]

		month_candidates = []
		day_candidates = []
		hour_candidates = []

		while not self.is_complete():
			# finding a month
			while not self.month:
				for m in months:
					month_candidates += re.findall(months[m][0], inpt)

				# if all goes well
				if len(month_candidates) == 1:
					self.month = month_candidates[0]
					#break
				
				# if we pick up more than one month name 
				elif len(month_candidates) > 1:
					a = randint(0, len(no_comprendo)-1)
					b = randint(0, len(ask_again) - 1)
					inpt = input('\n'.join([no_comprendo[a].format('month'),
								ask_again[b], '> ']))

				# if we do not find any month names
				elif len(month_candidates) < 1:
					a = randint(0, len(no_comprendo)-1)
					b = randint(0, len(ask_again) - 1)
					inpt = input('\n'.join([no_comprendo[a].format('month'),
								ask_again[b], '> ']))

			# finding day
			while not self.day:
				for d in days:
					day_candidates += re.findall(days[d][0], inpt)

				if len(day_candidates) == 1:
					self.day = day_candidates[0]
				
				# if we pick up more than one day name 
				elif len(day_candidates) > 1:
					a = randint(0, len(no_comprendo)-1)
					b = randint(0, len(ask_again) - 1)
					inpt = input('\n'.join([no_comprendo[a].format('day'),
								ask_again[b], '> ']))
				
				# if we do not find any day names
				elif len(day_candidates) < 1:
					a = randint(0, len(no_comprendo)-1)
					b = randint(0, len(ask_again) - 1)
					inpt = input('\n'.join([no_comprendo[a].format('day'),
								ask_again[b], '> ']))
			# finding hour
			while not self.hour:
				for d in days:
					hour_candidates += re.findall(hours[d], inpt)

				if len(hour_candidates) == 1:
					self.hour = hour_candidates[0]
				
				# if we pick up more than one day name 
				elif len(hour_candidates) > 1:
					a = randint(0, len(no_comprendo)-1)
					b = randint(0, len(ask_again) - 1)
					inpt = input('\n'.join([no_comprendo[a].format('time'),
								ask_again[b], '> ']))
				
				# if we do not find any day names
				elif len(hour_candidates) < 1:
					a = randint(0, len(no_comprendo)-1)
					b = randint(0, len(ask_again) - 1)
					inpt = input('\n'.join([no_comprendo[a].format('time'),
								ask_again[b], '> ']))
		else:
			return True

	def display(self):
		'''just for development purposes, can be rewritten later to do
		something more prodictive.
		'''
		print(self.month, self.day, self.date, self.hour)
		return "{} {}".format(self.month, self.day)
	
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


class Conversation:
	def __init__(self, states):
		self.states = states
		self.state = 'greeting'
		self.events = [Event()]

	def parse_input(self, r):
		e = self.events[-1]
		p = e.is_complete()
		e.details(r)
		if e.is_empty() or p:
			score = pos_or_neg(r)
			if score > 0:
				if self.state == 'make-another': self.events.append(Event())
				return ('boolean', True)
			elif score < 0:
				return ('boolean', False)
			else:
				if r == 'hi':
					return ('greeting', None)
				if r == "exit":
					return ('exit', None)
		elif e.is_complete():
			return ('appointment', e)
		elif not e.is_empty():
			e.interrogate(r)
			return ('appointment', e)
		return ('null', None)

	def output(self, event):
		outputs = self.states[self.state][0]
		if type(event) != type(True) and type(event) != type(None):
			print(type(event))
			return outputs[randint(0, len(outputs)-1)].format(event.display())
		else:
			return outputs[randint(0, len(outputs)-1)]

	# determine the next state, print the current state's output, and change to next state
	def next_state(self, response, response_type):
		rt = response_type

		# tuple-encoded state-option: (true-state, false-state)
		if type(self.states[self.state][1][rt[0]]) == type(()):
			if response_type[1]:
				self.state = self.states[self.state][1][rt[0]][0]
			else:
				self.state = self.states[self.state][1][rt[0]][1]
		else:
			self.state = self.states[self.state][1][rt[0]]

		# single string means state alias (different output, same behaviour)
		if type(prags[self.state][1]) == type(''):
			out = self.output(response_type[1])
			self.state = self.states[self.state][1]
			return out
		else:
			return self.output(response_type[1])

	def parse(self, r):
		rt = self.parse_input(r)
		if DEBUG: print("! %s: type(%s): %s" % (self.state, rt, r))
		if rt[0] in self.states[self.state][1]:
			#self.read_input(r, rt)
			return self.next_state(r, rt)
		elif rt[0] == 'exit':
			return False
		else:
			return "I'm sorry, I don't understand \"{}\"...".format(r)

c = Conversation(prags)
while 1:
	s = input("> ")
	l = c.parse(s)
	if l: print(l)
	else: break
	