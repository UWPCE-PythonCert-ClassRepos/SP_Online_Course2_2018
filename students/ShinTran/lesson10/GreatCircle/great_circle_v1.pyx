'''
Shin Tran
Python 220
Assignment 10

Dig into the compile and link steps required by Cython
Using some C functions/Cython
'''

import math

def great_circle(double lon1, double lat1, double lon2, double lat2):
    cdef double a, b, theta, c, x, radius

    radius = 3956 # miles
    x = math.pi/180.0
    a = (90 - lat1) * (x)
    b = (90 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))
    return radius * c

def great_circle_loop(double lon1, double lat1, double lon2, double lat2):
    for i in range(1000000):
        great_circle(lon1, lat1, lon2, lat2)
