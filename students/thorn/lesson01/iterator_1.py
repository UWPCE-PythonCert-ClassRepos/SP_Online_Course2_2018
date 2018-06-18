"""
Simple iterator examples
"""


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


class IterateMe_2(IterateMe_1):
    def __init__(self, start, stop=5, step=1):
        self.start = start
        self.stop = stop
        self.step = step
        self.current = start - step

    def __next__(self):
        """
        Add the step to current number.  Return current if less than stop number (want 1 before stop).  Raise StopIteration if over stop.
        """
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration


if __name__ == "__main__":
    # print("Testing the iterator")
    # for i in IterateMe_1():
    #     print(i)

    it = IterateMe_2(2, 20, 2)
    for i in it:
        if i > 10:
            break
        print(i)

    for i in it:
        print(i)

    zero_thru_8_by_two = IterateMe_2(0, 10, 2)
    test_list = list(zero_thru_8_by_two)
    print(test_list)
    assert test_list == [i for i in range(0, 10, 2)]

    three_thru_eighteen_by_three = IterateMe_2(3, 21, 3)
    test_list = list(three_thru_eighteen_by_three)
    print(test_list)
    assert test_list == [i for i in range(3, 21, 3)]