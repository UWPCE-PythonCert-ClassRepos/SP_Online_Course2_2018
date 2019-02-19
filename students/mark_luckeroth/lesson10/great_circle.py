
# from great_circle_v0 import great_circle
# from great_circle_v1 import great_circle
# from great_circle_v2 import great_circle
# from great_circle_v3 import great_circle
# from great_circle_v4 import great_circle
import timeit

SETUP = """
from great_circle_v1 import great_circle
lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 54.826
"""

TEST_CODE = """
great_circle(lon1, lat1, lon2, lat2)
"""

if __name__ == "__main__":
    runtimes = timeit.repeat(setup = SETUP, stmt = TEST_CODE, repeat=3, number=10000000)
    print('Duration1 = {} \nDuration2 = {} \nDuration3 = {}'.format(*runtimes))