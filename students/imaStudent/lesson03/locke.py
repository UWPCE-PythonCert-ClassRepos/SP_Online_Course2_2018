
class Locke:

    def __init__(self, capacity):
        self.capacity = capacity

    def __enter__(self):
        print("Stopping the pumps")
        print("Opening the doors")
        return self

    def move_boats_through(self, boats):
        if self.capacity < boats:
            raise Exception("CapacityException")
        else:
            print("Moving boats through")

    def __exit__(self, type, value, traceback):
        if type is Exception and str(value) == "CapacityException":
            print("!!! Maximum Capacity Exceeded !!!")
        print("Closing the doors")
        print("Restarting the pumps\n")
        return True

if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)

    # A lock with sufficient capacity can move boats without incident.
    with large_locke as locke:
        locke.move_boats_through(boats)
