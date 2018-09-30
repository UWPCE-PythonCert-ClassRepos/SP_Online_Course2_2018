# ----------------------------------------------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: iterator_1.py
# DATE CREATED: original class object IterateMe_1 created by instructor and accessed on 08/15/2018
# UPDATED: 08/15/2018
# PURPOSE: Working on the concept of iterators and iterables
# DESCRIPTION:  Class objects defining iteration behavior for assignment. IterateMe_1 shows the functionality of the
# object to act as the range() object utilizing a start, stop, and step modus; the child to the parent-class
# IterateMe_1 - IterateMe_2 - operates similarly to its parent class but with the ability to start, stop, and step from
# any user-input via its configurations in the overriden methods __iter__() and __next__().
# The __iter__() object behaves similarly to the range() function in function however on running both under the same
# conditions, the range() function is capable of picking up from the break-point of the for-loop while the iterator
# object that was created does not behave this way. Further reading on the subject yields the discussion of the differ-
# -ences between the two and how range() is NOT an iterator even though it does iterate over information in a similar
# fashion. See: http://treyhunner.com/2018/02/python-range-is-not-an-iterator/
# ----------------------------------------------------------------------------------------------------------------------


#  =============================================    SET UP    =======================================================
# No imports
#  ==================================================================================================================


#  ============================================    PROCESSING    ====================================================
spacing = '\n' * 2


class IterateMe_1:
	"""
	Returns sequence from 1 - 4
	"""

	def __init__(self, stop=5):
		self.current = -1
		self.stop = stop

	def __iter__(self):
		return self

	def __next__(self):
		self.current += 1
		if self.current < self.stop:
			return self.current
		else:
			raise StopIteration


class IterateMe_2(IterateMe_1):
	"""
	Iterator requires user determination of start/stop and has default step of 1.
	Will iterate over a list of integers from start to stop at the rate of
	the step input.
	"""
	def __init__(self, start, stop, step=1):
		self.current = start - step
		self.start = start
		self.step = step
		super().__init__(stop=stop)

	def __iter__(self):
		self.current = self. start - self.step
		return self

	def __next__(self):
		self.current += self.step
		if self.current < self.stop:
			return self.current
		else:
			raise StopIteration
#  ==================================================================================================================


#  ==============================================    OUT-PUT    =====================================================


if __name__ == "__main__":

	print("Testing the iterator: ")
	for i in IterateMe_1():
		print(i)

	print("Testing the second iterator: ")
	for i in IterateMe_2(2, 21, 2):
		print(i)

	print(spacing)

	# start stop
	print("Test stopping iteration and starting again: ")
	it = iter(IterateMe_2(10, 100, 10))
	for i in it:
		if i == 60:
			print('Break Point')
			break
		print(i)
	for i in it:
		print(i)

	print(spacing)

	print("Range() Test")
	my_iter = iter(range(10, 100, 10))
	for i in my_iter:
		if i == 60:
			print('Break')
			print(i)
			break
		print(i)
	for i in my_iter:
		print(i)
#  ==================================================================================================================
