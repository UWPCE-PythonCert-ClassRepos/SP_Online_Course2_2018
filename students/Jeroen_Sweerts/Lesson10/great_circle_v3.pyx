import cython
import time 

cdef extern from "math.h":
    float cosf(float theta)
    float sinf(float theta)
    float acosf(float theta)
    
lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 54.826


cdef float _great_circle_raw(float lon1,float lat1,float lon2,float lat2):
    cdef float radius = 3956.0 
    cdef float pi = 3.14159265
    cdef float x = pi/180.0
    cdef float a,b,theta,c

    a = (90.0-lat1)*(x)
    b = (90.0-lat2)*(x)
    theta = (lon2-lon1)*(x)
    c = acosf((cosf(a)*cosf(b)) + (sinf(a)*sinf(b)*cosf(theta)))
    return radius*c

def great_circle_raw(float lon1,float lat1,float lon2,float lat2):
    cdef int i
    cdef float x
    for i in range(10000000):
        x = _great_circle_raw(lon1,lat1,lon2,lat2)
    return x