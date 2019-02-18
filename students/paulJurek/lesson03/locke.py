"""the locke represents the Lock behavior for the ballard locks.  
This is bassed of Lesson 3 of Python 220
https://startlearning.uw.edu/courses/course-v1:UW+PYTHON220+2018_Spring/courseware/087092567db6485c9fa5ee7d1a528a6e/75d801b4fd124e209fc2f37f2b1d405e/
"""

class Locke:
    """representation of nautical lock system"""
    def __init__(self, boat_capacity:int, locke_state: str='low'):
        """args:
            boat_capacity: positive integer or 0 representing the max boat
                count the locke can process
            lock_state: enumeration indication if locke is low or high"""
        self.boat_capacity = boat_capacity

    def __enter__(self):
        print('run pumps')
        print('open door1')
        print('moving boats')
        print('closing door1')
        print('starting pumps')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type != None:
            print(f"Exception found: {exc_val}")
        return True

    def move_boats_through(self, boats: int, boat_level: str = 'low') -> bool:
        """processes boats through locke.
        args:
            boats: positive or 0 int representing boats trying to come through locke
            boat_level: high or low.  indicates starting level of boat entry
        returns:
            boolean indicating if transfer was successful"""
        if ((boats % 1) > 0) | (boats < 0) :
            raise ValueError('invalid input for number of boats')
        if (boats > self.boat_capacity):
            boats = self.boat_capacity
            self.move_boats_through(boats=boats)
            raise ValueError(f'too many boats going through locks. {boats} successfully moved through locks.')
        else:
            print(f'moving {boats} boats through locks')
        return True
        

if __name__=="__main__":
    locke = Locke(5)
    with locke:
        locke.move_boats_through(6)