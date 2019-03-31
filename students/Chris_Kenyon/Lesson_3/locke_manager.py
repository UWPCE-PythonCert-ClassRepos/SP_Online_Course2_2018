#!/usr/bin/env python3
#Lesson 3: Context Manager

from time import sleep


class Locke:
    def __init__(self, capacity=0):
        self.capacity = capacity

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, e_tb):
        if e_type:
            print(e_val)
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
            sleep(num_boats)            
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