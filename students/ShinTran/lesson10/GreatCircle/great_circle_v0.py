'''
Shin Tran
Python 220
Assignment 10

Play with Cython and the Great Circle code!
Using pure straight forward Python
'''

import math

def great_circle(lon1, lat1, lon2, lat2):
    radius = 3956 # miles
    x = math.pi/180.0
    a = (90 - lat1) * (x)
    b = (90 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))
    return radius * c

def great_circle_loop(lon1, lat1, lon2, lat2):
    for i in range(1000000):
        great_circle(lon1, lat1, lon2, lat2)
