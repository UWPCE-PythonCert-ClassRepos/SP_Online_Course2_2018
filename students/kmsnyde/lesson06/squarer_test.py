# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 14:00:50 2018

@author: Karl M. Snyder
"""

from squarer import Squarer

class SquarerTest():
    
    @staticmethod
    
            result = Squarer.calc(num)
            
            if result != square:
                print("Squared {} and got {} but expected {}.".format(num,
                      result, square))
                
    @staticmethod
    def test_negative_numbers():
        squares = {-1: 1,
                   -2: 4,
                   -3: 9,
                   -12: 144,
                   -100: 10000}
        
        for num, square in squares.items():
            result = Squarer.calc(num)
            
            if result != square:
                print("Squared {} and got {} but expected {}.".format(num,
                      result, square))
                
if __name__ == '__main__':
    SquarerTest.test_positive_numbers()
    SquarerTest.test_negative_numbers()