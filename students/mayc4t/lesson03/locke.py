#FileID:  locke.py

#!/usr/bin/env python3

class Locke(object):
    
    def __init__(self, max_boats):
        print ('ENTER __init__')
        self._max_boats = max_boats

    def __enter__(self):
        print ('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print ('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
        return True

    def _stop_pumps(self):
        print('Stopping the pumps.')

    def _open_doors(self):
        print('\tOpening the doors.')

    def _close_doors(self):
        print('\tClosing the doors.')

    def _restart_pumps(self):
        print('\tRestarting the pumps.')

    def move_boats_through(self, num_boats):
        for boat_idx in range(num_boats):
            if boat_idx >= self._max_boats:
                raise RuntimeError('Locke at capacity!')
            self._stop_pumps()
            self._open_doors()
            self._close_doors()
            self._restart_pumps()


small_locke = Locke(5)
large_locke = Locke(10)
boats = 8

# Too many boats through a small locke will raise an exception
print('Test small locke.')
with small_locke as locke:
    locke.move_boats_through(boats)

# A lock with sufficient capacity can move boats without incident.
print('\n\n\n\n')
print('Test large locke.')
with large_locke as locke:
    locke.move_boats_through(boats)
