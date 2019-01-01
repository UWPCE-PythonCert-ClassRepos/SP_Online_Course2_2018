cdef extern from "math.h":
    double cos(double x)
    double sin(double x)
    double acos(double x)


cpdef double great_circle_optimize3(double lon1, double lat1, double lon2,
double
lat2):
    cdef double a, b, theta, c, x, radius
    cdef double pi = 3.141593

    radius = 3956
    x = pi / 180.0
    a = (90.0 - lat1) * x
    b = (90.0 - lat2) * x
    theta = (lon2 - lon1) * x
    c = acos((cos(a) * cos(b)) + (sin(a) * sin(b) * cos(theta)))
    return radius * c

