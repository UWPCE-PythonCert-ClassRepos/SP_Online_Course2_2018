# ----------------------------------------------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: Locke.py
# DATE CREATED: 09/25/2018
# UPDATED: 09/26/2018
# PURPOSE: PYTHON 201 -- Assignment 3, Context Managers
# DESCRIPTION: Program uses context-manager-with-statements along with class Locke to simulate the processes
# of the Locke's functioning under day-to-day operations. If too many boats are in a locke (depending on its-
# - allocated size limits) the method passage() will raise a ValueError to display alerting the user to this
# problem.
#
# Fredrik Lundh's blog 'Understanding Python's "with" statement' (http://effbot.org/zone/python-with-statement.htm)
# came in-handy when working on this project, so I wanted to list that as a research source.
# ------------------------------------------------------------------------------------------------------------------

#  =============================================    SET UP    =======================================================
from termcolor import cprint

#  ============================================    PROCESSING    ====================================================


class Locke:
	"""
	Context manager class:
	Minimum Criteria:
	__init__()
	__enter__()
	__exit__()
	"""

	def __init__(self, locke_capacity):
		"""
		:param locke_capacity: Passed-in from __main__ as Locke's max allowable size
		"""
		self.locke_capacity = locke_capacity
		self.boats = 0  # var self.boats initialized to 0

	def __enter__(self):  # context_guard
		return self  # assigns what __enter__ returns to the variable in context mngr

	def passage(self, boat_traffic):
		"""
		:param boat_traffic: boats entering in passed-in from __main__
		:return: returns either ValueError or print statements before __exit__()
		"""
		self.boats = boat_traffic  # Locke object "boats" no longer set to 0
		if self.boats > self.locke_capacity:  # if boats entering Locke exceed capacity, error
			raise ValueError()

		else:  # print through Locke operations
			print("Stopping Locke Pumps")
			print("Opening Locke Doors >> boats enter")
			print("Closing Locke Doors (boats inside Locke)")
			print("Starting Locke Pumps")

	def __exit__(self, exception_type, exception_value, exception_traceback):
		"""
		:param exception_type: ValueError (if raised)
		:param exception_value: None or ValueError
		:param exception_traceback:
		:return: print messages below
		"""
		if exception_type is None:  # If no exceptions are raised, print Locke exit operations
			print("All clear!")
			print("Stopping Locke Pumps")
			print("Opening Locke Doors >> boats exit")
			print("Closing Locke Doors (Locke empty)")
			print("Starting Locke Pumps\n")
		elif exception_type is ValueError:  # if error is raised, print reason
			cprint("ValueError: Number of ships exceeds locke's "
				"capacity by {}".format(self.boats - self.locke_capacity), 'red')

#  ==============================================    OUT-PUT    =====================================================


if __name__ == "__main__":
	small_Locke = Locke(5)  # Locke capacity for small_Locke (returned in __enter__ as self)
	large_Locke = Locke(10)  # Locke capacity for large_Locke (returned in __enter__ as self)

	with small_Locke as obj:  # context manager (with self.small_locke_capacity as itself)
		obj.passage(2)  # locke_capacity.passage(boat_traffic(2))

	with large_Locke as large_obj:  # context manager (with self.large_locke_capacity as itself)
		large_obj.passage(8)  # locke_capacity.passage(boat_traffic(8))

	# This will raise ValueError exception
	with large_Locke as fail_test:  # context manager (with self.large_locke_capacity as itself)
		fail_test.passage(32)  # locke_capacity.passage(boat_traffic(32))
