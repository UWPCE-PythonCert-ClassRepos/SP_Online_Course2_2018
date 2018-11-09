class Locke:
    ''' Write a context manager class Locke to simulate the overall functioning of the system. 
    When the locke is entered it stops the pumps, opens the doors, closes the doors, and restarts the pumps. Likewise when the locke is exited it runs through the same steps: 
    it stops the pumps, opens the doors, closes the doors, and restarts the pumps. '''

    def __init__(self, boats):
        self.boats = boats

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(exc_val) 
        return True

    def move_boats_through(self, num_boats):
        if num_boats < self.boats:
            print("\nStopping the pumps...\nOpening the doors...\nClosing the doors...\nRestarting the pumps...\n")
        else:
            raise ValueError ("\nToo many boats for this size locke, sorry\n")


if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 9

    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)

    # A lock with sufficient capacity can move boats without incident.
    with large_locke as locke:
        locke.move_boats_through(boats)
