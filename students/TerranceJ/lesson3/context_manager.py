"""
Lesson 3 Context Manager Assignment
Terrance J
2/28/2019
"""

class Locke:
    
    def __init__(self,max_boats):
        self.max_boats = max_boats
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(exc_val)
            return True

    def move_boats_through(self, num_boats):
        print('Maximum boat capacity: {}'.format(self.max_boats))
        if num_boats < self.max_boats:
            print('Number of boats below capacity. Proceed!')
            print('Stopping the pumps')
            print('Opening the doors')
            print('Closing the doors')
            print('Starting the pumps')
        else:
            raise ValueError('Number of boats is above capcity. Cannot proceed!')
print(__name__)

if __name__ == '__main__':
    boats = 8
    small_locke = Locke(5)
    large_locke = Locke(10)

    with small_locke as locke:
        locke.move_boats_through(boats)
    print()

    with large_locke as locke:
        locke.move_boats_through(boats)
