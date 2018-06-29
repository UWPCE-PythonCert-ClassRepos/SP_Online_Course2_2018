#!/usr/bin/env python3


from contextlib import contextmanager

def pump_handler(func):
    def wrapper(*args, **kwargs):
        print("Stopping the pumps.")
        result = func(*args, **kwargs)
        print("Restarting the pumps.")
        return result
    return wrapper

def door_handler(func):
    def wrapper(*args, **kwargs):
        print("Opening the doors.")
        result = func(*args, **kwargs)
        print("Closing the doors.")
        return result
    return wrapper

class Locke:
    def __init__(self, capacity):
        self.capacity = capacity
    
    def __enter__(self):
        self.locke_function_process()
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        if e_type == ValueError:
            print(e_value)
        return self.locke_function_process()

    @pump_handler
    @door_handler
    def locke_function_process(self):
        return True

    def move_boats_through(self, num_boats):
        if num_boats > self.capacity:
            raise ValueError(f"Aborting - number of boats passing through "
                    f"({num_boats}) exceeds locke capacity ({self.capacity}).")
        else:
            print(f"{num_boats} boats passing through the locke.")


if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    print("\n\n\t *** Small locke - 5-boat capacity: *** \n")
    with small_locke as locke:
        locke.move_boats_through(boats)

    print("\n\n\t *** Large locke - 10-boat capacity: *** \n")
    with large_locke as locke:
        locke.move_boats_through(boats)
