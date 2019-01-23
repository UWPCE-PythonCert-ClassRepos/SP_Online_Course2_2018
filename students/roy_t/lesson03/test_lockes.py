#!/usr/bin/env python3


__author__ = 'roy_t githubtater'

import unittest
import lockes
import io
import sys


class TestLockes(unittest.TestCase):

	def setUp(self):
		self.small_locke_size = 5
		self.large_locke_size = 10
		self.small_locke = lockes.Locke(self.small_locke_size)
		self.large_locke = lockes.Locke(self.large_locke_size)
		self.boats = 8

	def test_locke_can_only_be_initialized_with_integer(self):
		assert ValueError(lockes.Locke('asdf'))
		assert TypeError(lockes.Locke([1, 2, 3, 4]))

	def test_locke_is_properly_initialized(self):
		self.assertIsInstance(self.small_locke, lockes.Locke)

	def test_locke_initialized_with_correct_capacity(self):
		# small_locke capacity should not be equal to large locke size
		self.assertNotEqual(self.small_locke.capacity, self.large_locke_size)
		# small_locke.capacity should always equal the size it was initiated with
		self.assertEqual(self.small_locke.capacity, self.small_locke_size)

	def test_too_many_boats_for_locke_capacity(self):
		with self.assertRaises(ValueError):
			self.small_locke.move_boats_through(self.boats)

	def test_boats_enter_locke(self):
		for boat in range(1, 2):
			with self.large_locke as locke:
				locke.move_boats_through(12)

	def test_engage_locke_takes_correct_steps_when_entering(self):
		# create an object to read stdout
		captured_output = io.StringIO()
		sys.stdout = captured_output
		# enter the locke
		self.large_locke.engage_locke(entering=True)

		# We expect the following actions when boats enter the locke
		expected_text = '''Enter: Stopping the pumps.
Enter: Opening the doors.
Move: Boats entering the locke.
Exit: Closing the doors.
Exit: Restarting the pumps.
'''
		self.assertEqual(captured_output.getvalue(), expected_text)

	def test_engage_locke_takes_correct_steps_when_exiting(self):
		# create object to read stdout
		captured_output = io.StringIO()
		sys.stdout = captured_output

		expected_text = '''Enter: Stopping the pumps.
Enter: Opening the doors.
Exit: Boats exiting the locke
Exit: Closing the doors.
Exit: Restarting the pumps.
'''
		# engage the locke: exiting
		self.large_locke.engage_locke(entering=False)
		self.assertEqual(captured_output.getvalue(), expected_text)

	def tearDown(self):
		print('Tearing down...')


if __name__ == '__main__':
	unittest.main()
