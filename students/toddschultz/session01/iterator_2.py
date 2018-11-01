def iterator_2(start, stop, step=1):
	while start < stop:
		yield start
		start = start+step

qwerty = iterator_2(10, 30, 3)
for i in qwerty:
	print(i)
