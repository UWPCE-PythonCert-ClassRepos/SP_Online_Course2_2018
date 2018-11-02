#!/usr/bin/env python3
import time


class locke():

    def __init__(self, boats):
        self.max_boats = boats

    def __enter__(self):
        print("Locke size is: " + str(self.max_boats))
        time.sleep(1)
        print("\n...Stopping the pumps...")
        time.sleep(1)
        print("\n...Opening the doors...")
        time.sleep(1)
        return self

    def __exit__(self, type, value, traceback):

        if(type == ValueError):
            print("\nToo many boats!")
            error_string = "\nThis locke can only handle a max number of {} boats."
            print(error_string.format(self.max_boats))

        print("\n...Closing the doors...")
        time.sleep(1)
        print("\n...Restarting the pumps...\n")
        print("-"*20+"\n")
        return True

    def move_boats_through(self, boats):

        if(boats > self.max_boats):
            raise ValueError()
        else:
            print("\n" + "##### " + str(boats) + " boats moving through! #####")


if __name__ == "__main__":
    small_locke = locke(3)
    medium_locke = locke(5)
    large_locke = locke(10)

    boats = 5

    with large_locke as locke:
        # print("\nTest #1")
        locke.move_boats_through(boats)

    with small_locke as locke:
        # print("\nTest #2")
        locke.move_boats_through(boats)

    with medium_locke as locke:
        # print("\nTest #1")
        locke.move_boats_through(boats)
