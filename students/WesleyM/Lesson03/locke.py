class Locke:
    def __init__(self, boats):
        self.boats = boats
    
    def __enter__(self):
        print("Stopping the pumps.")
        print("Opening the doors.")
        return self

    def __exit__(self, *args):
        return None

    def move_boats_through(self, num_boats):
        if num_boats < self.boats:
            print("Closing the doors.")
            print("Restarting the pumps.")
        else:
            raise Exception('Too many boats. Over capacity.')

small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    locke.move_boats_through(boats)

# Too many boats through a small locke will raise an exception
with small_locke as locke:
    locke.move_boats_through(boats)
