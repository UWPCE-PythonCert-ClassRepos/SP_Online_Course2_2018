import cython
import time 

cdef extern from "math.h":
    float cosf(float theta)
    float sinf(float theta)
    float acosf(float theta)
    
lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 54.826


def great_circle_raw(double lon1, double lat1, double lon2, double lat2):
    cdef double radius, x, a, b, theta,c, pi    
    radius = 3956 # miles
    pi = 3.14159265
    x = pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = acosf((cosf(a)*cosf(b)) + (sinf(a)*sinf(b)*cosf(theta)))  
    return radius * c

