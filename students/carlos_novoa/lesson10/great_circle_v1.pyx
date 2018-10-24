"""
Great Circle - Defined arguments
"""

import math


def great_circle(double lon1, double lat1, double lon2, double lat2):

    radius = 3956  # miles
    x = math.pi / 180.00
    a = (90.00 - lat1) * (x)
    b = (90.00 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = math.acos((math.cos(a) * math.cos(b)) +
                  (math.sin(a) * math.sin(b) * math.cos(theta)))
    return radius * c
