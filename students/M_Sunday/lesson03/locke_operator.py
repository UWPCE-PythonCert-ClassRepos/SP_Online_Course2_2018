class TooManyBoats(Exception):
    def __init__(self, max_boats):
        self.max_boats = max_boats


class Locke:

    def __init__(self, boat_limit):
        self.boat_limit = boat_limit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # returning None allows for a clean exit
        return None

    def move_boats_through(self, boat_count):
        if boat_count > self.boat_limit:
            raise TooManyBoats("There are too many boats in the Locke, "
                               "the maximum number of boats allowed is {"
                               "}".format(self.boat_limit))
        else:
            print("-----Moving {} boats through the Locke-----\n"
                  "             Stopping the pumps.           \n"
                  "             Opening the doors.            \n"
                  "             Closing the doors.            \n"
                  "             Restarting the pumps.         \n"
                  "-----------Boat Transfer Complete---------".
                  format(boat_count))


def operator():
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    with small_locke as locke:
        locke.move_boats_through(boats)

    with large_locke as locke:
        locke.move_boats_through(boats)


if __name__ == "__main__":
    operator()
