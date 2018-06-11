from time import sleep


class Locke:
    def __init__(self, capacity=0):
        self.capacity = capacity

    def __enter__(self):
        #print('Now in enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #print('Now in Exit\n\n')
        if exc_type:
            print(exc_val)
        return True
    
    def move_boats_through(self, num_boats):
        if num_boats > self.capacity:
            raise ValueError('Too many boats for the locke')
        else:
            print("Stopping the pumps")
            sleep(1)
            print("Opening the doors")
            sleep(1)
            print("Letting the boats in")
            sleep(num_boats/2)
            print("Closing the doors")
            sleep(1)
            print("Restarting the pumps")
            sleep(1)


if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    with small_locke as locke:
        locke.move_boats_through(boats)

    with large_locke as locke:
        locke.move_boats_through(boats)
