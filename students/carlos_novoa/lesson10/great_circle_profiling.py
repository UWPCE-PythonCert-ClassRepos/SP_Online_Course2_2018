import math
import time
from timeit import timeit as timer


# from memory_profiler import profile
lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 54.826
repetitions = 100000


# @profile
def great_circle_raw(lon1, lat1, lon2, lat2):
    radius = 3956  # miles
    x = math.pi / 180.00
    a = (90.00 - lat1) * (x)
    b = (90.00 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = math.acos((math.cos(a) * math.cos(b)) +
                  (math.sin(a) * math.sin(b) * math.cos(theta)))
    return radius * c


def calculate_acos(a, b, theta):
    return math.acos((math.cos(a) * math.cos(b)) +
                     (math.sin(a) * math.sin(b) * math.cos(theta)))


def great_circle_acos(lon1, lat1, lon2, lat2):
    radius = 3956  # miles
    x = math.pi / 180.0
    a = (90.0 - lat1) * (x)
    b = (90.0 - lat2) * (x)
    theta = (lon2 - lon1) * (x)
    c = calculate_acos(a, b, theta)
    return radius * c


def calculate_x():
    return math.pi / 180.0


def calculate_coordinate(lat, x):
    return (90.0 - lat) * x


def calculate_theta(lon2, lon1, x):
    return (lon2 - lon1) * x


def great_circle_factored(lon1, lat1, lon2, lat2):
    radius = 3956  # miles
    x = calculate_x()
    a = calculate_coordinate(lat1, x)
    b = calculate_coordinate(lat2, x)
    theta = calculate_theta(lon2, lon1, x)
    c = calculate_acos(a, b, theta)
    return radius * c


if __name__ == '__main__':
    # python -m memory_profiler great_circle_profiling.py

    great_circle_raw(lon1, lat1, lon2, lat2)
    # great_circle_acos(lon1, lat1, lon2, lat2)
    # great_circle_factored(lon1, lat1, lon2, lat2)

    # print("\n\nRaw function")
    # print(timer(
    #     'great_circle_raw(lon1, lat1, lon2, lat2)',
    #     globals=globals(),
    #     number=repetitions
    # ))

    # print("\n\nAcos factored")
    # print(timer(
    #     'great_circle_acos(lon1, lat1, lon2, lat2)',
    #     globals=globals(),
    #     number=repetitions
    # ))

    # print("\n\nEverything factored")
    # print(timer(
    #     'great_circle_factored(lon1, lat1, lon2, lat2)',
    #     globals=globals(),
    #     number=repetitions
    # ))
    # print("\n\n")

    # print("\n\nRaw function")
    # init = time.clock()
    # great_circle_raw(lon1, lat1, lon2, lat2)
    # print("Took this long: %s" % (time.clock() - init))

    # print("\n\nAcos factored")
    # init = time.clock()
    # great_circle_acos(lon1, lat1, lon2, lat2)
    # print("Took this long: %s" % (time.clock() - init))

    # print("\n\nEverything factored")
    # init = time.clock()
    # great_circle_factored(lon1, lat1, lon2, lat2)
    # print("Took this long: %s" % (time.clock() - init))
    # print("\n\n")
