class Locke:
    def __init__(self, limit_boat):
        self.limit_boat = limit_boat

    def __enter__(self):
        return self

    def __exit__(self, etype, evalue, tb):
        if etype == ValueError:
            print("WARNING: Too many boats through.")

    def  move_boats_through(self, number_boats):
        if number_boats <= self.limit_boat:
            print("Stopping the pumps.")
            print("Opening the doors.")
            print("Closing the doors.")
            print("Restarting the pumps.")
        else:
            raise ValueError

if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    with small_locke as locke:
        locke.move_boats_through(boats)

    with large_locke as locke:
        locke.move_boats_through(boats)
