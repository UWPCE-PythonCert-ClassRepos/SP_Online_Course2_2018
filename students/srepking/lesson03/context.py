class Locke():
    """
        Write a context manager class Locke to simulate the overall functioning of the system.
        When the locke is entered it stops the pumps, opens the doors, closes the doors, and
        restarts the pumps. Likewise when the locke is exited it runs through the same steps:
        it stops the pumps, opens the doors, closes the doors, and restarts the pumps.During
        initialization the context manager class accepts the locke’s capacity in number of boats.
        Raise error if someone tries to move too many boats through the locke. Print what is
        happening with the doors and pumps.

        Too many boats through a small locke will raise an exception
        with small_locke as locke:
            locke.move_boats_through(boats)

        A Locke with sufficient capacity can move boats without incident.
            "Stopping the pumps."
            "Opening the doors."
            "Closing the doors."
            "Restarting the pumps."
    """


    def __init__(self, locke_size):
        print('This Locke can handle {} boats.'.format(locke_size))
        self.size = locke_size

    def __enter__(self):
        print('Entering the Locke.\n'
              'Stop the pumps.\n'
              'Opening the doors.\n'
              'Closing the doors.\n'
              'Restarting the pumps.')
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        #print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
        if exc_type is ValueError:
            print('Too many boats in Locke. Locke will not operate.')
            return self
        else:
            print('Exiting the Locke.\n'
              'Stop the pump.\n'
              'Opening the doors.\n'
              'Closing the doors.\n'
              'Restarting the pumps.')
        return True

    def move_boats_through(self, num_boats):
        if num_boats > self.size:
            raise ValueError()

