""" Write a context manager class named "Locke"
    WHen locked entered:
        stop pump
        opens doors
        closes doors
        restarts pumps
    When Locke exited:
        stops pumps
        opens doors
        closes doors
        restarts pumps
    
    class initiation:
        class accepts locke's capacity (num boats)

    if too many boats:
        error raised

Example:
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)

    # A lock with sufficient capacity can move boats without incident.
    with large_locke as locke:
        locke.move_boats_through(boats)
 """

class Locke:
    def __init__(self, capacity):
        self.capacity = capacity

    def __enter__(self):

    
    def __exit__(self):