#!/usr/bin/env python3


__author__ = "roy_t githubtater"

from contextlib import contextmanager


def doors(func):
	def wrapper(*args, **kwargs):
		print('Enter: Opening the doors.')
		result = func(*args, **kwargs)
		print('Exit: Closing the doors.')
		return result
	return wrapper


def pumps(func):
	def wrapper(*args, **kwargs):
		print('\nEnter: Stopping the pumps.')
		result = func(*args, **kwargs)
		print('Exit: Restarting the pumps.')
		return result
	return wrapper


class Locke:
	"""Context manager for moving boats through the Lockes"""

	def __init__(self, capacity):
		"""Each locke is initialized with a given capacity"""
		try:
			self.capacity = int(capacity)
			self.queue = 0
		except ValueError as e:
			print('Error: ' + str(e))
		except TypeError as e:
			print('Error: ' + str(e))

	def __enter__(self):
		"""Take actions when entering locke"""
		self.engage_locke(True)
		return self

	def __exit__(self, type, value, traceback):
		"""Take actions when exiting locke"""
		if type == ValueError:
			print(value)
		self.engage_locke(False)
		if self.queue > 0:
			with Locke(self.capacity) as locke:
				locke.move_boats_through(self.queue)
		return True

	@pumps
	@doors
	def engage_locke(self, entering=True):
		"""Take specific actions depending on boats entering/exiting locke"""
		if entering:
			print('Move: Boats entering the locke.')
		else:
			print('Exit: Boats exiting the locke')

	def move_boats_through(self, boats):
		"""
		Move boats through the locke.
		:param boats: Number of boats requesting to move through the locke
		:return: None
		"""
		# Verify the number of boats does not exceed the locke capacity
		if boats > self.capacity:
			self.queue = boats - self.capacity
			raise ValueError(f'The number of boats requested ({boats}) exceeds locke capacity ({self.capacity})'\
							 f'\nAllowing {self.capacity} boats to pass ({self.queue} boats remaining in queue)')

		else:
			# move boats through the locke
			print(f'Move: {boats} boat(s) going through the locke.')


def main():
	# initiate a locke that can move 5 boats through
	small_locke = Locke(5)

	# initialize a bigger locke for moving boats through
	large_locke = Locke(10)
	boats = 8

	# move boats through the small locke
	print(f'\n**** Moving {boats} boats through small locke. Capacity = {small_locke.capacity} boats.')
	with small_locke as locke:
		locke.move_boats_through(boats)

	# move boats through the large locke
	print(f'\n**** Moving {boats} boats through large locke. Capacity = {large_locke.capacity} boats.')
	with large_locke as locke:
		locke.move_boats_through(boats)


if __name__ == '__main__':
	main()
