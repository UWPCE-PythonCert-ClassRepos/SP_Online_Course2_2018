"""
File Name: locke_class.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 1/31/2019
Python Version: 3.6.4
"""


class Locke:
    def __init__(self, capacity):
        self.capacity = capacity
        self.boats_in_lock = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print(exc_value)
        else:
            self.stop_pumping()
            self.open_doors()
            self.boats_exit()
            self.close_doors()
        return True

    def test_capacity(self, count):
        print('Testing Capacity')
        if count > self.capacity:
            raise OverflowError('Attempt would exceed capacity').with_traceback(None)
        else:
            print('Within Capacity')

    def move_boats_through(self, count):
        self.test_capacity(count)
        self.stop_pumping()
        self.open_doors()
        self.boats_enter()
        self.close_doors()
        self.start_pumping()


    def start_pumping(self):
        print('Starting Pumping')

    def stop_pumping(self):
        print('Stopping Pumping')

    def open_doors(self):
        print('Opening doors')

    def close_doors(self):
        print('Closing doors')

    def boats_enter(self):
        print('Boats entering lock')

    def boats_exit(self):
        print('Boats leaving locke')
