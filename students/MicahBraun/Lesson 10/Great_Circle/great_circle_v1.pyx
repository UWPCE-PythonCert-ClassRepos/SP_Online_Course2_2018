# -------------------------------------------------------------------------------------
# PROJECT NAME: great_circle_v1.py
# NAME: Micah Braun
# DATE CREATED: 11/30/2018
# UPDATED:
# PURPOSE: Lesson 10 final
# DESCRIPTION: Function is optimized for the C/static language by:
#              - importing specific items from math instead
#                of "math.x"
#              - declaring types in function parameters
#              - declaring all variables' types
#
# ON RUN: Program took 4.655s to complete processes on 64-bit OS with 16 GB RAM
# -------------------------------------------------------------------------------------
from math import pi as PI, acos, cos, sin


# -- Version 1 --
def great_circle(double lon1, double lat1, double lon2, double lat2):
    cdef double a, b, c, radius, theta, x
    radius = 3956    # miles
    x = PI/180.0
    a = (90.0-lat1)*(x)
    b = (90.0-lat2)*(x)
    theta = (lon2-lon1)*(x)
    c = acos((cos(a)*cos(b))+(sin(a)*sin(b)*cos(theta)))

    return radius*c
