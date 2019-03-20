#!/usr/bin/env python3

# Cython version using cdef extern to import math functions

from libc.math cimport M_PI


cdef extern from "math.h":
    float sinf(float x)
    float cosf(float x)
    float acosf(float x)


def great_circle(float lon1, float lat1, float lon2, float lat2):
    cdef float radius, x, a, b, theta, c

    radius = 3956  # miles
    x = M_PI / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = get_theta(lon1, lon2, x)

    c = acosf((cosf(a) * cosf(b)) + (sinf(a) * sinf(b) * cosf(theta)))

    return radius * c


cdef float get_theta(float lon1, float lon2, float x):
    return ((lon2 - lon1) * (x))
