# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 18:14:23 2018

@author: Karl M. Snyder
"""

class Locke:
    def __init__(self, size):
        self.size = size
                
    def __enter__(self):
        return self
    
    
    def move_boats(self, num_boats):
        self.boats = num_boats
        if self.boats > self.size:
            raise ValueError("You have too many boats for the size of your locke.  Locke size is {} boats; munber of boats is {}.".format(self.size,
                             self.boats))
        else:
            print("'Stopping the pumps.'\n'Opening the door.'\n'Closing the doors.'\n'Restarting the pumps.'")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("\nYour boats made it into the Locke!\n\n")
        
if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    
    # These work
    with small_locke as locke:
        locke.move_boats(4)
    
    with large_locke as locke:
        locke.move_boats(8)
    
    # This throws an exception
    with large_locke as locke:
        locke.move_boats(11)
