"""
Generator assigment for lesson 1
"""

def intsum():
	"""keep adiding the next integer.
	"""
	n = 0
	sum = 0
	
	while True:
		sum += n
		yield sum
		n +=1

def intsum2():
	n = 0
	sum = 0
	
	while True:
		sum += n
		yield sum
		n +=1

"""
Doubler- 1,2,4,8,16 .....
"""
def doubler():
	"""Each value is double the previous"""
	start = 1
	while True:
		yield start
		start *= 2

"""
Fibonacci sequence
"""
def fib():
	n1, n2 = 1,1
	while True:
		yield n1
		n1, n2 = n2, n1 + n2

"""
Prime numbers
"""
def prime():
	"""Generate prime numbers"""
	num = 2
	while True:
		if num < 2 or not [a for a in range(2, num) if num % a == 0]:
			yield num
		num += 1



