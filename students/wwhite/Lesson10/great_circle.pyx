# from libc.math cimport sin
# from libc.math cimport cos
# from libc.math cimport pi
# from libc.math cimport acos

cdef extern from "math.h":
    double sin(double x)
cdef extern from "math.h":
    double cos(double x)
cdef extern from "math.h":
    double pi
cdef extern from "math.h":
    double acos(double x)

cpdef double great_circle(double lon1, double lat1, double lon2, double lat2):
    cdef double a, b, c, radius, theta, x

    radius = 3956
    x = pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = acos((cos(a) * cos(b)) + (sin(a) * sin(b) * cos(theta)))
    return radius * c

    # cdef extern produced a lower runtime than calling cdef with cpdef
