'''
Lesson 3 Assignment #1
Conext Managers
'''

class Locke:

    def __init__(self, capacity):
        print(('capacity = {}').format(capacity))
        self.capacity = capacity

    def __enter__(self):
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__({},{},{})'.format(exc_type,exc_val,exc_tb))
        return self.capacity

    def move_boats_through(self, boats):
        print(('Number of boats = {}').format(boats))
        if boats > self.capacity:
            raise Exception("Operation is cancelled.")
        else:
            print("Proceed operation...")
            print("Stopping the pumps")
            print("Opening the doors")
            print("Closing the doors")
            print("Restarting the pump")       


def main():
    with small_locke as locke:
        locke.move_boats_through(boats)

    with large_locke as locke:
        locke.move_boats_through(boats)


small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

if __name__ == '__main__':
    main()


