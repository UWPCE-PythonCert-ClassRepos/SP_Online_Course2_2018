from libc.math cimport acos
from libc.math cimport sin
from libc.math cimport cos


def great_circle(float lon1, float lat1, float lon2, float lat2):
    cdef float a, b, theta, c, x, radius, result

    radius = 3956. #miles
    x = 3.14156 / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = acos((cos(a) * cos(b)) + (sin(a) * sin(b) * cos(theta)))
    result = radius * c
    return result