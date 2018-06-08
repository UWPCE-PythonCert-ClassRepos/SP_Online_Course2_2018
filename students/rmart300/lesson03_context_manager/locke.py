class Locke:

    def __init__(self, max_boats):
        self.max_boats = max_boats

    def __enter__(self):
        print("Stopping the pumps.")
        print("Opening the doors.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        exception_found = False
        if exc_type is ValueError:
            print('{}, {}, {}'.format(exc_type, exc_val, exc_tb))
            exception_found = True

        print("Closing the doors.")
        print("Starting the pumps.")
        return exception_found

    def move_boats_through(self, boats):

        if boats > self.max_boats:
            raise ValueError("too many boats for locke")

    
