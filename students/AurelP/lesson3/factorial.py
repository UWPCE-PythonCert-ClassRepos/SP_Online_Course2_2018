
#!/usr/bin/python
#Lesson 3 Aurel Perianu

"""
	factorial recurssive
"""

def factorial(nr):
	"""
	 factorial recurssive
	"""
	if nr != 1:
		return nr*factorial(nr-1)
	return 1

if __name__ == "__main__":
	for i in range(1, 7):
		print("factorial of:{} is:{}\n".format(i,str(factorial(i))))
