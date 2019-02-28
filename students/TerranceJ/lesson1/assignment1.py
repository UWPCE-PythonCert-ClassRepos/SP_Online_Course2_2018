"""Lesson 1 assignment
	written by Terrance J
"""

#COMPREHENSION ASSIGNMENT
def top_five():
	"""This is the comprehensions assignment
	Return the top 5 tracks meeting loudness and danceability
	"""

	music = pandas.read_csv("featuresdf.csv")

	results = [(d,l,n,a) for d,l,n,a in zip(music.danceability,music.loudness, music.name,music.artists)]  

	new_results = []

	for i in results:
		if i[0] > 0.8:
			if i[1] < -5.0:
				new_results.append(i)

	new_results = sorted(new_results, reverse = True)

	top_five =  new_results[:5]

	return top_five

#ITERATOR ASSIGNMENT
class IterateMe_2:
	
	def __init__(self, start, stop, step):
		self.current = start
		self.stop = stop
		self.step = step

	def __iter__(self):
		return self

	def next(self):
		if self.current<self.stop:
			self.current += self.step
			return self.current
		else:
			raise StopIteration

def my_range(start,end):
	current = start
	while current < end:
		yield current
		current += 1

"""num = my_range(1,10)
print(next(num))
print(next(num))"""

"""it = IterateMe_2(2,20,2)
for i in it:
	if i > 10: break
	print(i)
print "this is the break"

for i in it:
	print(i)"""

"""If you break from the loop of an iterator, it will stop. when you pick it up again, 
it remembers its state and picks up where it left of at the break.
Range Does not behave the same as an iterator. it does not pick up where the break occurs"""


#GENERATOR ASSIGNMENT

def sum_of_integers(stop):
	"""GENERATOR - keep adding the next integer"""
	x = 0
	y = 1
	while y < stop:
		z = x + y
		x = z
		yield z
		y += 1

def doubler(stop):
	"""GENERATOR - Each value is double the previous value"""
	n = 1
	count = 0
	while count < stop:
		yield n
		n = n + n
		count += 1

def fibonacci(stop):
	"""GENERATOR - fibonacci sequence"""
	count = 0
	n1 = 0
	n2 = 1
	while count < stop:
		n3 = n1 + n2
		yield n3
		#update variables
		n1 = n2
		n2 = n3
		count += 1






