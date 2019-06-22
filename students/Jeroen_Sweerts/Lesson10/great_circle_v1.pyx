import math
import cython


import time 
lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 54.826


def great_circle_raw(double lon1, double lat1, double lon2, double lat2):
    cdef double radius, x, a, b, theta,c    
    radius = 3956 # miles
    x = math.pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))    
    return radius * c

def calculate_acos(a, b, theta):
    return math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))

def great_circle_acos(lon1, lat1, lon2, lat2):
    radius = 3956 # miles
    x = math.pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    theta = (lon2 - lon1) * (x)
#     c = math.acos((math.cos(a) * math.cos(b)) + (math.sin(a) * math.sin(b) * math.cos(theta)))
    c = calculate_acos(a, b, theta)
    return radius * c
    
def calculate_x():
    return math.pi * 180.0

def calculate_coordinate(lat, x):
    return (90.0 - lat) * x

def calculate_theta(lon2, lon1, x):
    return (lon2 - lon1) * x

def great_circle_factored(lon1, lat1, lon2, lat2):
    radius = 3956 # miles
    x = calculate_x()
    a = calculate_coordinate(lat1, x)
    b = calculate_coordinate(lat2, x)
    theta = calculate_theta(lon2, lon1, x)
    c = calculate_acos(a, b, theta)
    return radius * c
