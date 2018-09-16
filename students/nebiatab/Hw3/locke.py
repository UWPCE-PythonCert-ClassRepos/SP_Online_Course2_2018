class Locke:

  def __init__(self, capacity):
    self.capacity = capacity

  def __enter__(self):
    return self

 

  def move_boats_through(self, boats):
    self.boats = boats
    if boats < self.capacity:
      print("Stopping Pumps.")
      print("Opening Doors.")
      print("Closing Doors.")
      print("Restart Pumps.")
    else:
      raise Exception("Too many boats.")

  def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type is Exception:
      print(exc_val)


   

small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

# Too many boats through a small locke will raise an exception
#with small_locke as locke:
#    locke.move_boats_through(boats)

# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    locke.move_boats_through(boats)

