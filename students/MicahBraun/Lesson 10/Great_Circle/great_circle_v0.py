# -------------------------------------------------------------------------------------
# PROJECT NAME: great_circle_v0.py
# NAME: Micah Braun
# DATE CREATED: 11/30/2018
# UPDATED: 
# PURPOSE: Lesson 10 final
# DESCRIPTION: Function is left un-optimized for the C/static language (no type dec-
#              -larations before assignment, standard Python library imports.
#              This is the first run to get time benchmarks on further optimizations.
#
# ON RUN: Program took 8.130s to complete processes on 64-bit OS with 16 GB RAM
# -------------------------------------------------------------------------------------
import math


# -- Version 0 --
def great_circle(lon1, lat1, lon2, lat2):
    radius = 3956    # miles
    x = math.pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))

    return radius * c
