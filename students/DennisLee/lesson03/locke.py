#!/usr/bin/env python3


from contextlib import contextmanager

def pump_handler(func):
    def wrapper(*args, **kwargs):
        print("\nStopping the pumps.")
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
        self.queue = 0
    
    def __enter__(self):
        self.locke_function_process(True)
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        if e_type == ValueError:
            print(e_value)
        self.locke_function_process(False)
        if self.queue > 0:
            with Locke(self.capacity) as locke:
                locke.move_boats_through(self.queue)
        return True

    @pump_handler
    @door_handler
    def locke_function_process(self, entering=True):
        if entering:
            print("Boats entering locke.")
        else:
            print("Boats exiting locke.")

    def move_boats_through(self, num_boats):
        self.queue = max(0, num_boats - self.capacity)
        if self.queue > 0:
            raise ValueError(f"Number of boats trying to pass ({num_boats}) "
                    f"exceeds locke capacity ({self.capacity}). {self.queue} "
                    f"boat(s) are waiting for next passage cycle.")
        else:
            print(f"{num_boats} boat(s) passing through the locke.")


if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)

    for boats in range(2, 27, 6):
        print(f"\n\n\t ***Small locke, {boats} boat(s) attempting passage:***")
        with small_locke as locke:
            locke.move_boats_through(boats)

        print(f"\n\n\t ***Large locke, {boats} boat(s) attempting passage:***")
        with large_locke as locke:
            locke.move_boats_through(boats)
