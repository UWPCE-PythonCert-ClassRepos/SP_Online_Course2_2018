#!/usr/bin/env python3


class locke():

    def __init__(self, max_boats):
        self.max_boats = max_boats

    def __enter__(self):
        print("Stopping the pumps.")
        print("Opening the doors.")
        return self

    def __exit__(self, e_type, e_val, e_traceback):
        unsuccessful_transfer = False
        if e_type == ValueError:
            print('The transfer failed due to there being too many boats.')
            print('{} \n{}, {}.'.format(e_val, e_type, e_traceback))
            unsuccessful_transfer = True
        print("Closing the doors.")
        print("Starting the pumps.")
        return unsuccessful_transfer

    def move_boats_through(self, boats):
        if boats > self.max_boats:
            raise ValueError('There are {} boats. '
                             'The max is {}.'.format(boats, self.max_boats))
        print("{} boats are moving through.".format(boats))


if __name__ == '__main__':
    small_locke = locke(5)
    large_locke = locke(10)

# small locke succeeds
    print('\n5 Boats are here!')
    with small_locke as locke:
        locke.move_boats_through(5)

# small locke fails
    print('\n8 Boats are here!')
    with small_locke as locke:
        locke.move_boats_through(8)

# large locke succeeds
    print('\n8 Boats are here!')
    with large_locke as locke:
        locke.move_boats_through(8)

# large locke fails
    print('\n12 Boats are here!')
    with large_locke as locke:
        locke.move_boats_through(12)
