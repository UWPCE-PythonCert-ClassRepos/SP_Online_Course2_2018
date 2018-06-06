from locke import Locke

small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

def message(boats, max_boats):
    print(f"moving {boats} boats through ballard lock with capacity {max_boats}")

# Too many boats through a small locke will raise an exception
with small_locke as new_locke:
    message(boats, new_locke.max_boats)
    new_locke.move_boats_through(boats)

# A lock with sufficient capacity can move boats without incident.
with large_locke as new_locke:
    message(boats, new_locke.max_boats)
    new_locke.move_boats_through(boats)
