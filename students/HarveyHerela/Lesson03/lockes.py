class Locke:
    
    def __init__(self, boat_limit):
        self.boat_limit = boat_limit
    
    
    def __enter__(self):
        return self
    
    
    def move_boats_through(self, boats):
        if boats > self.boat_limit:
            raise OverflowError(f"Locke only fits {self.boat_limit} boats. {boats} boats won't fit.")
        print("Stopping the pumps.")
        print("Opening the doors.")
        print("Closing the doors.")
        print("Restarting the pumps.")    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == None:
            return True
        elif exc_type == OverflowError:
            print(exc_val)
            return True
        else:
            return False
    
    
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
    