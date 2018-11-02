'''
Sean Tasaki
10/25/2018
Lesson03
'''

import random

class Locke:
    def __init__(self, boat_lim, boats):
        self.boat_lim = boat_lim
        self.boats = boats
    
    def __enter__(self):
        print("Entering locke.")
        print("Attempting to move {} boats through the locke.".format(self.boats))
        if self.boats > self.boat_lim:
            raise Exception(f"The boat limit for this locke has been exceeded!\n{self.boat_lim} boats can fit and there are {self.boats} in the locke.\n")
        return self
       
    def boats_moving_through(self):       
        print("Stopping the pumps.\nOpening the doors.\nClosing the doors.\nRestarting the pumps.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == None:
            print("Exiting locke successfully")
            print("Stopping the pumps.\nOpening the doors.\nClosing the doors.\nRestarting the pumps.")               
            return True
        elif exc_type == Exception:
            print(exc_val)
            return True
        else:
            return False

if __name__ == "__main__":

    num_of_boats = random.randint(1, 12)


    #Small lockes have a limit of 5 boats.
    small_locke = Locke(5, num_of_boats)

    #large lockes have a limit of 10 boats.
    large_locke = Locke(10, num_of_boats)

    '''
    large locke is upstream of small locke, so
    large locke scenario runs first.
    '''

    with large_locke as locke:
        locke.boats_moving_through()
       
    with small_locke as locke:
        locke.boats_moving_through()
        
    

