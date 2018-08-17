"""
Locke class for lesson 3
"""

class Locke:
    def __init__(self, capacity, handle_exception):
        self.capacity = capacity
        self.handle_exception = handle_exception
        
    def move_boats_through(self, num_boats):
        if num_boats <= self.capacity:
            print('Stopping the pumps')
            print('Opening the doors')
            print('Closing the doors')
            print('Restarting the pumps')
        else:
            raise ValueError('Number of boats exceeds locke capacity')

    def __enter__(self):
        return self
    
    def __exit__(self, ex_type, ex_value, ex_traceback):
        
        if ex_type==ValueError:
            print(ex_value)
        return self.handle_exception
    

if __name__ == '__main__':
    small_locke = Locke(5, True)
    with small_locke as locke:
        locke.move_boats_through(8)




