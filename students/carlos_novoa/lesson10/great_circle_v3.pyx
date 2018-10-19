# cython: profile=True

"""
Great Circle
    Optimizations:
    - Define argument types
    - memoization
    - remove python math and import C math
    - reduce precision by replacing double with float
    - remove PI and predefine x
"""


cdef extern from "math.h":
    float cosf(float)
    float sinf(float)
    float acosf(float)


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
def great_circle(float lon1, float lat1, float lon2, float lat2):
    cdef float radius = 3956  # miles
    cdef float x = 565.48667772
    cdef float a, b, theta, c

    a = (90.0 - lat1) * x
    b = (90.0 - lat2) * x
    theta = (lon2 - lon1) * x

    c = acosf((cosf(a)*cosf(b)) + (sinf(a)*sinf(b)*cosf(theta)))
    return radius * c
