#!/usr/bin/env python3


from contextlib import contextmanager

# @contextmanager
def pump_handler(func):
    def wrapper(*args, **kwargs):
        print("Stopping the pumps.")
        result = func(*args, **kwargs)
        # yield
        print("Restarting the pumps.")
        return result
    return wrapper

# @contextmanager
def door_handler(func):
    def wrapper(*args, **kwargs):
        print("Opening the doors.")
        result = func(*args, **kwargs)
        # yield
        print("Closing the doors.")
        return result
    return wrapper

class Locke:
    def __init__(self, capacity):
        self.capacity = capacity
    
    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        if e_type == ValueError:
            print(e_value)
            return True

    @pump_handler
    @door_handler
    def move_boats_through(self, num_boats):
        if num_boats > self.capacity:
            raise ValueError(f"Number of boats passing through ({num_boats}) "
                    f"exceeds locke capacity ({self.capacity}).")
        else:
            print(f"{num_boats} boats passing through the locke.")

if __name__ == "__main__":
    boats = 8

    print("\n\t***Small locke - 5-boat capacity:***")
    with Locke(5) as small_locke:
        small_locke.move_boats_through(boats)

    print("\n\t***Large locke - 10-boat capacity:***")
    with Locke(10) as large_locke:
        large_locke.move_boats_through(boats)