"""
Great Circle - Defined arguments + memoization
"""

import math


class Memoize:
    """
    memoize decorator from avinash.vora
    http://avinashv.net/2008/04/python-decorators-syntactic-sugar/
    """
    def __init__(self, function):  # runs when memoize class is called
        self.function = function
        self.memoized = {}

    def __call__(self, *args):  # runs when memoize instance is called
        try:
            return self.memoized[args]
        except KeyError:
            self.memoized[args] = self.function(*args)
            return self.memoized[args]


@Memoize
def great_circle(double lon1, double lat1, double lon2, double lat2):

    radius = 3956  # miles
    x = math.pi / 180.00
    a = (90.00 - lat1) * (x)
    b = (90.00 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = math.acos((math.cos(a) * math.cos(b)) +
                  (math.sin(a) * math.sin(b) * math.cos(theta)))
    return radius * c