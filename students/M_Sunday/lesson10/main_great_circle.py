from great_circle_v0 import great_circle_raw
from great_circle_v1 import great_circle_optimize1
from great_circle_v2 import great_circle_optimize2
from great_circle_v3 import great_circle_optimize3
import time

if __name__ == "__main__":
    start = time.time()
    lon1g = -72.345
    lat1g = 34.323
    lon2g = -61.823
    lat2g = 54.826
    for i in range(10000000):
        great_circle_raw(lon1g, lat1g, lon2g, lat2g)
    print("Raw Great Circle code took {:.4f} seconds".format(time.time() -
                                                           start))

    start = time.time()
    lon1g = -72.345
    lat1g = 34.323
    lon2g = -61.823
    lat2g = 54.826
    for i in range(10000000):
        great_circle_optimize1(lon1g, lat1g, lon2g, lat2g)
    print("C defined variables: Great Circle code took {:.4f} seconds".format(
        time.time() -
                                                             start))

    start = time.time()
    lon1g = -72.345
    lat1g = 34.323
    lon2g = -61.823
    lat2g = 54.826
    for i in range(10000000):
        great_circle_optimize2(lon1g, lat1g, lon2g, lat2g)
    print("C defined variables and function inputs: Great Circle "
          "code took {:.4f} seconds".format(
        time.time() -
        start))


    start = time.time()
    lon1g = -72.345
    lat1g = 34.323
    lon2g = -61.823
    lat2g = 54.826
    for i in range(10000000):
        great_circle_optimize3(lon1g, lat1g, lon2g, lat2g)
    print("C defined variables, function inputs, and math functions: Great "
          "Circle code "
          "took {:.4f} "
          "seconds".format(
        time.time() -
        start))
