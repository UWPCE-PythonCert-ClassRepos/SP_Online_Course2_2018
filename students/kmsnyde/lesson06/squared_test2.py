# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 16:26:26 2018

@author: Karl M. Snyder
"""

import unittest

from squarer import Squarer

class SquarerTest(unittest.TestCase):
    
    def test_positive_numbers(self):
        
        squares = {1: 1,
                   2: 4,
                   3: 9,
                   12: 144,
                   100: 10000}
        
        for num, square in squares.items():
            self.assertEqual(square, Squarer.calc(num), "Squaring {}.".format(num));
            
    def test_negative_numbers(self):
         
        squares = {-1: 1,
                   -2: 4,
                   -3: 9,
                   -12: 144,
                   -100: 10000}
        
        for num, square in squares.items():
            self.assertEqual(square, Squarer.calc(num), "Squaring {}.".format(num));

if __name__ == "__main__":
    a = SquarerTest()
    a.test_positive_numbers()
    a.test_negative_numbers()