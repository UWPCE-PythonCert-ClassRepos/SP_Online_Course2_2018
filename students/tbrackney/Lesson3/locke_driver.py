"""
File Name: locke_driver.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 1/31/2019
Python Version: 3.6.4
"""

from locke_class import Locke


small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

# Too many boats through a small locke will raise an exception
with small_locke as locke:
    print('Attempting small lock')
    locke.move_boats_through(boats)

# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    print('Attempting large lock')
    locke.move_boats_through(boats)
