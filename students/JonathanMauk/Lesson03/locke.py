class Locke:

    def __init__(self, capacity):
        self.capacity = capacity

    def __enter__(self):
        print("---\nStopping the pumps.\nOpening the doors.")
        return self

    def move_boats_through(self, boats_count):
        print(f"{boats_count} boats entering locke with a capacity of {self.capacity}.")
        if boats_count > self.capacity:
            raise OverflowError("Number of boats exceeds locke capacity. Please try again.")
        print("Closing the doors.\nRestarting the pumps.")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            print("Stopping the pumps.\nOpening the doors.\nBoats exiting locke.")


if __name__ == "__main__":
    small_locke = Locke(5)
    medium_locke = Locke(8)
    large_locke = Locke(10)
    boats = 8

    # Should run without any issues.
    with large_locke as locke:
        locke.move_boats_through(boats)

    # Should run without any issues--this fills but does not exceed capacity.
    with medium_locke as locke:
        locke.move_boats_through(boats)

    # Should raise an exception.
    with small_locke as locke:
        locke.move_boats_through(boats)
