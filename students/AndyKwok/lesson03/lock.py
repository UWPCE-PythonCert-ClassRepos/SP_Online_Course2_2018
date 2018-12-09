# Author: Andy Kwok
# Last Updated: 11/11/18

#!/usr/bin/env python3

class Locke(object):
    def __init__(self, capacity):
        self.cap = capacity
        
    def move_boats_through(self, boat):
        if boat > self.cap:
            raise RuntimeError("The lock is over-loaded!")
        else:
            print("Stopping the pumps.")
            print("Opening the doors.")
            print("Closing the doors.")
            print("Restarting the pumps.")        
        

    def __enter__(self):
        print('__enter__()')
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
        return self.cap

if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8
   
    with small_locke as locke:
        locke.move_boats_through(boats)
    
    with large_locke as locke:
        locke.move_boats_through(boats)