import math
import numpy as np

def great_circle(double lon1, double lat1, double lon2, double lat2):
    cdef double a, b, theta, c, x, radius

    radius = 3956. #miles
    x = np.pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = np.arccos((np.cos(a) * np.cos(b)) + (np.sin(a) * np.sin(b) * np.cos(theta)))
    return radius * c