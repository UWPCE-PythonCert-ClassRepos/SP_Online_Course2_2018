#Jared Mulholland
#Homework 3

class Locke:

    def __init__(self, locke_capacity):
        self.locke_capacity = locke_capacity

    def __enter__(self):
        """When the locke is entered it stops the pumps, opens the doors, closes the doors, and restarts the pumps"""
        print("stop pumps")
        print("open doors")
        print("close doors")
        print("restart pumps")
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """when the locke is exited it runs through the same steps: it stops the pumps, opens the doors, closes the doors, and restarts the pumps"""
        if exception_type is ValueError:
            print(exception_value)
        else:
            print("stop pumps")
            print("open doors")
            print("close doors")
            print("restart pumps")
        return self

    def move_boats(self, boats):
        """If someone tries to move too many boats through the locke, anything over its established capacity, raise a suitable error"""
        if boats > self.locke_capacity:
            raise ValueError("Not enough room in the locke")

if __name__ == "__main__":
    small_locke = Locke(5)
    big_locke = Locke(10)
    boats = 8

    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats(boats)

    # A lock with sufficient capacity can move boats without incident.
    with big_locke as locke:
        locke.move_boats(boats)
 
