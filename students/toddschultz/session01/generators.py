def sum_gen(*args):
	'''keep adding the next integer'''
	yield sum(int(i) for i in args)

def double_gen(a): 
	'''Each value is double the previous value
	(a) number of values created'''
	count, num = 0, 1
	while count < a:
		yield num
		num = num * 2
		count += 1

def fib_gen(a):
	'''Fib sequence to (a) integers'''
	count, i = 1, [1, 1]
	while count < a-1:
		i.append(i[-2] + i[-1])
		yield i
		count += 1

def prime_gen(n):
	'''Generate all prime numbers up to (a)
	(numbers only divisible by them self and 1)'''
	p = 2
	while p < n-1:
		for i in range(2, p):
			if p%i == 0:
				p=p+1
		yield p 
		p=p+1


sums = sum_gen(1,2,34,5,6,7,7)
for i in sums:
	print(i)

print("``````````````````````````````````")

doubles = double_gen(10)
for i in doubles:
	print(i)

print("``````````````````````````````````")
fibs = fib_gen(4)
for i in fibs:
	print(i)

print("``````````````````````````````````")
primes = prime_gen(20)
for i in primes:
	print(i)

