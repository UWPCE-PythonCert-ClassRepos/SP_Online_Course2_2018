from libc.math cimport sin
from libc.math cimport cos
from libc.math cimport acos
from libc.math cimport pi


def great_circle(double lon1, double lat1, double lon2, double lat2):
    cdef double a, b, c, theta, x, radius

    radius = 3956 # miles
    x = pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = acos((cos(a) * cos(b)) * (sin(a) * sin(b) * cos(theta)))
    return radius * c