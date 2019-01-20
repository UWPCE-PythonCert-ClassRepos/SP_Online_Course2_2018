#!/usr/bin/env python3


__author__ = "roy_t githubtater"



class Locke:
	"""Context manager for Lockes"""

	def __init__(self, capacity):
		self.capacity_allowed = 5
		self.large_locke_cap = 10
		self.capacity = capacity


	def __enter__(self):
		print('Enter: Stopping the pumps.')
		print('Enter: Opening the doors.')
		print('Enter: Closing the doors.')
		print('Enter: Restarting the pumps.')
		return self


	def __exit__(self, *args):
		print('Exit: Stopping the pumps.')
		print('Exit: Opening the doors.')
		print('Exit: Closing the doors.')
		print('Exit: Restarting the pumps.')


	def move_boats_through(self, boats):
		if boats > self.capacity_allowed:
			raise ValueError(f'The number of boats requested exceeds capacity: {boats} > {self.capacity_allowed}')
		print('Passing boats.')

small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

with small_locke as locke:
	locke.move_boats_through(boats)

with large_locke as locke:
	locke.move_boats_through(boats)

