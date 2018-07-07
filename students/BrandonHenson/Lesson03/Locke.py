# Brandon Henson
# Python 220
# Lesson 3 Locke
# 7-6-18
# !/usr/bin/env python3


class Locke:

    def __init__(self, boats):
        self.boats = boats

    def __enter__(self):
        return self

    def move_boats_through(self, num_of_boats):
        if num_of_boats > self.boats:
            raise Exception('THIS IS TOO MANY BOATS!')
        else:
            print("STOPPING THE PUMPS.")
            print("OPENING THE DOORS.")
            print("CLOSING THE DOORS.")
            print("RESTARTING THE PUMPS.")

    def __exit__(self, *args):
        return None

if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8


with small_locke as locke:
    locke.move_boats_through(boats)


with large_locke as locke:
    locke.move_boats_through(boats)
