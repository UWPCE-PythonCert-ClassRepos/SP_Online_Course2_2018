# Great Circle exercise

import great_circle_v0
import great_circle_v1
import great_circle_v2

import timeit

lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 54.826

if __name__ == "__main__":
    num = 1000000
    t = timeit.Timer("great_circle_v0.great_circle_raw(%f,%f,%f,%f)" % (lon1,lat1,lon2,lat2),
                       "import great_circle_v0")
    print("Pure python function", t.timeit(num), "sec")
    t = timeit.Timer("great_circle_v1.great_circle(%f,%f,%f,%f)" % (lon1,lat1,lon2,lat2),
                       "import great_circle_v1")
    print("Cython function (still using python math)", t.timeit(num), "sec")
    t = timeit.Timer("great_circle_v2.great_circle(%f,%f,%f,%f)" % (lon1,lat1,lon2,lat2),
                       "import great_circle_v2")
    print("Cython function (using trig function from math.h)", t.timeit(num), "sec")
