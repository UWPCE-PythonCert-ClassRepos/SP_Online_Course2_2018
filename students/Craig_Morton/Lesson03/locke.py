# ------------------------------------------------- #
# Title: Lesson 3, Locke Assignment
# Dev:   Craig Morton
# Date:  11/25/2018
# Change Log: CraigM, 11/23/2018, Locke Assignment
# ------------------------------------------------- #

#!/usr/bin/env python3


class Locke:
    """Context Manager"""
    def __init__(self, capacity):
        self.capacity = capacity

    def __enter__(self):
        print("Stopping pumps.")
        print("Opening the doors.")
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        val = False
        if exception_type is ValueError:
            print(f'*Failure!  Could not pass boats: {exception_type}, {exception_value}, {exception_traceback}')
            val = True
        print("Closing doors.")
        print("Restarting pumps.")
        return val

    def pass_boats(self, boats):
        """Passes boats per defined value"""
        if boats > self.capacity:
            raise ValueError(f'Number of boats passing exceeds capacity: '
                             f'{boats}/{self.capacity}')
        print(f"Passing {boats} boats")


def main():
    """Main I/O"""
    small_locke = Locke(5)
    large_locke = Locke(10)

    # Pass boats successfully - Small locke
    with small_locke as locke:
        locke.pass_boats(4)

    # Too many boats exception - Small locke
    with small_locke as locke:
        locke.pass_boats(6)

    # Pass boats successfully - Large locke
    with large_locke as locke:
        locke.pass_boats(9)

    # Too many boats exception - Large locke
    with large_locke as locke:
        locke.pass_boats(15)


if __name__ == '__main__':
    main()
