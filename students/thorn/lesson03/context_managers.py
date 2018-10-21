"""
Thomas Horn

Lesson03 - Context Managers:
"""

'''
Context Manager (Locke):
- When locke is entered or exited:
    1. Stop pumps
    2. Open doors
    3. Close doors
    4. Restart pumps
- Init accepts:
    1. Locke's capacity in number of boats
- If too many boats attempted through the lock --> raise suitable error
- Print statements acceptable
'''

class Locke:
    def __init__(self, capacity=0, start_num_boats=0):
        self.capacity = capacity
        self.locke_boats = start_num_boats

    def __enter__(self):
        return self

    def move_boats_through(self, new_boats):
        # if new boats + current boats > capacity --> raise error
        self.locke_boats += new_boats
        if self.locke_boats > self.capacity:
            raise ValueError(f"Locke is over capacity.\n\t\tLocke Size: {self.capacity}\n\t\tTotal Boats: {self.locke_boats}")
        else:
            print("*Stopping Pumps*\n*Opening Doors*\n*Closing Doors*\n*Restarting Pumps*")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            print("Boats succesfully moved through the Locke.")

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