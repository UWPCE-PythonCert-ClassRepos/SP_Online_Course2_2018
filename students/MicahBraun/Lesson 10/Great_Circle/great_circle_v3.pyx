# -------------------------------------------------------------------------------------
# PROJECT NAME: great_circle_v0.py
# NAME: Micah Braun
# DATE CREATED: 11/30/2018
# UPDATED:
# PURPOSE: Lesson 10 final
# DESCRIPTION: Function is optimized for the C/static language by:
#              - Adding function wrapper to great_circle
#
# ON RUN: Program took 2.265s to complete processes on 64-bit OS with 16 GB RAM
# -------------------------------------------------------------------------------------
cdef extern from "math.h":
    float cosf(float theta)
    float sinf(float theta)
    float acosf(float theta)


# -- Version 3 --
cpdef double great_circle(double lon1,double lat1,double lon2,double lat2):
    cdef double a, b, c, radius, theta, x
    cdef double pi = 3.141592653589793
    # define pi out to x-num variables

    radius = 3956
    # miles

    x = pi/180.0
    a = (90.0-lat1)*(x)
    b = (90.0-lat2)*(x)
    theta = (lon2-lon1)*(x)
    c = acosf((cosf(a)*cosf(b))+(sinf(a)*sinf(b)*cosf(theta)))

    return radius*c