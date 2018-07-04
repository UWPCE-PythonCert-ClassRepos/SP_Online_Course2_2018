class Locke:

    def __init__(self, max_boats):
        self.max_boats = max_boats

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        no_boats = 0
        return no_boats

    def move_boats_through(self, current_boats):
        if current_boats > self.max_boats:
            raise Exception("Locke over capacity!")
        else:
            print("Stopping the pumps.")
            print("Opening the doors.")
            print("Closing the doors.")
            print("Restarting the pumps.")


small_locke = Locke(5)
large_locke = Locke(10)


with small_locke as locke:
    locke.move_boats_through(3)

with large_locke as locke:
    locke.move_boats_through(12)