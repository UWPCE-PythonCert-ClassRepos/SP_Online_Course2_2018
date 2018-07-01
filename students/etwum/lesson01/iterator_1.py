

class IterateMe_1:
    """
    About as simple an iterator as you can get:

    returns the sequence of numbers from zero to 4
    ( like range(4) )
    """

    def __init__(self, stop=5):
        self.current = -1
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

# extend class
class IterateMe_2(IterateMe_1):

    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step
        self.current = start - step

    def __iter__(self):
        # resets current
        self.current = self.start - self.step
        return self

    def __next__(self):
        # iterates through the range until the stop is reached
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":

    print("Testing the iterator")

    # prints 2 - 10 by 2; breaks after 10
    it2 = range(2,20,2)
    for i in it2:
        if i > 10:
            break
        print(i)

    # prints 2 - 18 by 2
    for i in it2:
        print(i)

    it = IterateMe_2(2, 20, 2)

    # matches range
    for i in it:
        if i > 10:
            break
        print(i)

    # matches range
    for i in it:
        print(i)