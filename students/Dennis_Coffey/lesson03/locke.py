# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 20:19:18 2019

@author: dennis
"""

""" The Locke Class - Lock behaviour of the Ballard Locks """

class Locke:
    
    def __init__(self, capacity):
        self.capacity = capacity
        
    def __enter__(self):
        # Opening doors and stopping pumps to let boats in
        print("Stopping the pumps.")
        print("Opening the doors.")
        return self
        
    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is ValueError:
            print(exception_value)
        else:
            # Close doors and restart pumps if number of boats is below capacity
            print("Closing the doors.")
            print("Restarting the pumps.")
        return True
        
    def move_boats_through(self, boats):
        if boats > self.capacity:
            raise ValueError("Number of boats exceeds the capacity of the lock, cannot close doors")
        
        
if __name__=="__main__":

    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8
    
    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)
    
    # A lock with sufficient capacity can move boats without incident.
    with large_locke as locke:
        locke.move_boats_through(boats)    