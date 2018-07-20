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
    def __init__(self, capacity=0):
        self.capacity = capacity

    def __enter__(self):
        return self
    

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