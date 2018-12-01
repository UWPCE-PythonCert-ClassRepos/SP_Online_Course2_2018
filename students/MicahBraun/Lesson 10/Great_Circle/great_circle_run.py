# -------------------------------------------------------------------------------------
# PROJECT NAME: great_circle_run.py
# NAME: Micah Braun
# DATE CREATED: 11/30/2018
# UPDATED:
# PURPOSE: Lesson 10 final
# DESCRIPTION: Run-file for great_circle Cython example and assignment option.
#              File imports corresponding .py or .pyx file and assigns values
#              to variables within the great_circle function.
#
# INFO: Written using PyCharm Professional Ed. on Windows 10 OS 64-bit system
#       All tests run using Ubuntu 18.04.1 LTS through bash on Windows.
# -------------------------------------------------------------------------------------

# from great_circle_v0 import great_circle
# from great_circle_v1 import great_circle
# from great_circle_v2 import great_circle
from great_circle_v3 import great_circle


lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 54.826


if __name__ == '__main__':
    for i in range(10000000):
        great_circle(lon1, lat1, lon2, lat2)

