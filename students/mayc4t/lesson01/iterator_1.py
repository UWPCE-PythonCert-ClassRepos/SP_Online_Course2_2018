#!/usr/bin/env python3

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

class IterateMe_2:
    """
    About as simple an iterator as you can get:

    """
    def reset(self,start, stop, step):
        self.current = start - step
        self.step = step
        self.stop = stop

    def __init__(self, start, stop, step):
        self.start_init = start
        self.stop_init = stop
        self.step_init = step
        self.reset(self.start_init, self.stop_init, self.step_init)

    def __iter__(self):
        self.reset(self.start_init, self.stop_init, self.step_init)
        #print ("IM2 {}, {}, {}".format(self.current, self.step, self.stop))
        return self

    def __next__(self):
        self.current += self.step
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

    def dbg(self):
        print('current=%s stop=%s' % (self.current, self.stop))

if __name__ == "__main__":

    it = IterateMe_2(start=5, stop=15, step=2)
    #it.dbg()

    print ("==== Testing IterateMe_2 =====")
    for i in it:
        if i > 10: break
        print ("\t{}".format(i))


    print("\t-- next after break --")
    for i in it:
        print ("\t{}".format(i))


    print ("\n\n==== range ==== " )
    irange = range(5,15,2)
    for i in irange:
        if i > 10: break
        print ("\t{}".format(i))
    
    print("\t-- next after break -- in range")
    for i in irange:
        print ("\t{}".format(i))
