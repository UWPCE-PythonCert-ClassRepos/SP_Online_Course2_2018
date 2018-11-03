# lesson 03 locke exercise
# !/usr/bin/env python3


def manage_tourists():
    print("\tManaging the tourists.")

def start_pumps():
    print("\tStarting the pumps.")

def stop_pumps():
    print("\tStopping the pumps.")

def open_doors():
    print("\tOpening the doors.")

def close_doors():
    print("\tClosing the doors.")


class Locke():
    def __init__(self, cap):
        self.cap = cap
    
    def __enter__(self):
        return self
        
    def __exit__(self, e_type, e_val, e_traceback):
        if e_type == None:
            return True
        elif e_type == Exception:
            print(e_val)
            return True
        else:
            return False
        
    def move_boats(self, cap):
        if cap < self.cap:
            print("Preparing to move {} boats.".format(cap))
            manage_tourists()
            start_pumps()
            stop_pumps()
            open_doors()
            close_doors()
        else:
            raise Exception("\tQueue of {} boats exceeds locke capacity.\n".format(cap))

            
def main():        
    small_locke = Locke(5)
    large_locke = Locke(10)

    with small_locke as locke:
        print("Using small locke:")
        locke.move_boats(3)
        print("")

    with large_locke as locke:
        print("Using large locke:")
        locke.move_boats(7)
        print("")
        
    with small_locke as locke:
        print("Overflowing small locke:")
        locke.move_boats(6)
        print("")
        
    with large_locke as locke:
        print("Overflowing large locke:")
        locke.move_boats(12)
        print("")


if __name__ == "__main__":
    main()