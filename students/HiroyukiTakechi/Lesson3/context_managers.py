'''
Lesson 3 Assignment #1
Conext Managers
'''


class Locke(object):

    def __init__(self, boats):
        print(('Number of boats = {}').format(boats))
        self.boats = boats


    def move_boats_throughs(self):
        pass


    def __enter__(self):
        print('__enter__()')
        print("Stopping the pumps")
        print("Opening the doors")
        print("Closing the doors")
        print("Restarting the pump")
        return self

    def __exit__(self):
        print('__exit__()')
        return self

def main():
    with small_locke as locke:
        locke.move_boats_through(boats)

    with large_locke as locke:
        locke.move_boats_through(boats)

if __main__ == '__main__':
    main()


import contextlib

@contextlib.contextmanager

def Locke(object):
    print('enter')
    
    try:
        print("Stopping the pumps")
        yield
        print("Opening the doors")
        yield
        print("Closing the doors")
        yield
        print("Restarting the pump")
    except:
        raise Exception('Error')
    finally:
        print('exit')

def main():
    with Locke():
        raise Exception('Error')

if __name__ == '__main__':
    main()


small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

# Too many boats through a small locke will raise an exception
with small_locke as locke:
    locke.move_boats_through(boats)

# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    locke.move_boats_through(boats)
