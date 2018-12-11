class Locke:

    def __init__(self, size):
        print("Initializing lock system...")
        self.size = size
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            pass
        else:
            print("Please reduce number of boats.")
        return

    def move_boats_through(self, boats):
        self.boats = boats
        if self.boats > self.size:
            raise RuntimeError
        else:
            print("Stopping the pumps")
            print("Opening the doors")
            print("Closing the doors")
            print("Restarting the pumps")
            print(f'{boats} boats have entered!')
            print("Stopping the pumps")
            print("Opening the doors")
            print("Closing the doors")
            print("Restarting the pumps")
            print(f'{boats} boats have exited!')