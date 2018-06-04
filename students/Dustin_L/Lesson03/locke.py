#!/usr/bin/env python3
"""Ballard Lock Module"""


class Locke:
    """Locke Context Manager"""
    def __init__(self, capacity):
        self.capacity = capacity

    def __enter__(self):
        print("Stopping pumps...")
        print("Opening the doors...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        retVal = False
        if exc_type is ValueError:
            print(f'Boat Transfer Failed: {exc_type}, {exc_val}, {exc_tb}')
            retVal = True

        print("Closing doors...")
        print("Restarting pumps...")
        return retVal

    def move_boats(self, num_boats):
        """Attempts to transfer number of specified boats.

        Args:
            num_boats (int): Number of boats to transfer.

        Raises:
            ValueError: Number of boats exceeds the capacity of the locke
        """
        if num_boats > self.capacity:
            raise ValueError(f'Number of boats exceeds capacity: '
                             f'{num_boats}/{self.capacity}')
        print(f"Transporting {num_boats} boats...")


def main():
    """Main function"""
    small_locke = Locke(5)
    large_locke = Locke(10)

    # Successfully moves boats
    with small_locke as locke:
        locke.move_boats(3)

    # Raises too many boats exception
    with small_locke as locke:
        locke.move_boats(6)

    # Sucessfully moves boats
    with large_locke as locke:
        locke.move_boats(8)

    # Raises too many boats exception
    with large_locke as locke:
        locke.move_boats(12)


if __name__ == '__main__':
    main()
