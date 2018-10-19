class Locke:

    def __init__(self, capacity):
        self.capacity = capacity

    def __enter__(self):
        return self

    def __exit__(self):
        return self

    def move_boats_through(self):
        return self


if __name__ == "__main__":
    small_locke = Locke(5)
    medium_locke = Locke(8)
    large_locke = Locke(10)
    boats = 8

    # Should raise an exception.
    with small_locke as locke:
        locke.move_boats_through(boats)

    # Should run without any issues--this fills but does not exceed capacity.
    with medium_locke as locke:
        locke.move_boats_through(boats)

    # Should run without any issues.
    with large_locke as locke:
        locke.move_boats_through(boats)
