from locke_operator import *
import io


def t_move_boats_through():

    # Test #1
    print("-----Moving 5 boats through the Locke-----\n"
          "             Stopping the pumps.           \n"
          "             Opening the doors.            \n"
          "             Closing the doors.            \n"
          "             Restarting the pumps.         \n"
          "-----------Boat Transfer Complete---------")
    expected = io.StringIO()

    locke_set = Locke(7)
    boats = 5

    with locke_set as locke:
        locke.move_boats_through(boats)

    actual = io.StringIO()
    assert actual.getvalue() == expected.getvalue()


    # Test #2
    print("-----Moving 1 boats through the Locke-----\n"
          "             Stopping the pumps.           \n"
          "             Opening the doors.            \n"
          "             Closing the doors.            \n"
          "             Restarting the pumps.         \n"
          "-----------Boat Transfer Complete---------")
    expected = io.StringIO()

    locke_set = Locke(7)
    boats = 1

    with locke_set as locke:
        locke.move_boats_through(boats)

    actual = io.StringIO()
    assert actual.getvalue() == expected.getvalue()


    # Test #3
    locke_set = Locke(5)
    boats = 7

    with locke_set as locke:
        locke.move_boats_through(boats)

    actual = io.StringIO()
    assert TooManyBoats


if __name__ == "__main__":
    t_move_boats_through()