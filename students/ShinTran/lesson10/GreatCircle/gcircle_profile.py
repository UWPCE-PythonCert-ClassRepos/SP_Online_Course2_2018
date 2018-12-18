'''
Shin Tran
Python 220
Assignment 10

Work with Cython profiling
'''

import pstats, cProfile

import great_circle_v0
import great_circle_v1
import great_circle_v2

params = [-72.345, 34.323, -61.823, 54.826]


cProfile.runctx("great_circle_v0.great_circle_loop({},{},{},{})".format(*params),
    globals(), locals(), "Profile0.prof")
s0 = pstats.Stats("Profile0.prof")
s0.strip_dirs().sort_stats("time").print_stats()

cProfile.runctx("great_circle_v1.great_circle_loop({},{},{},{})".format(*params),
    globals(), locals(), "Profile1.prof")
s1 = pstats.Stats("Profile1.prof")
s1.strip_dirs().sort_stats("time").print_stats()

cProfile.runctx("great_circle_v2.great_circle_loop({},{},{},{})".format(*params),
    globals(), locals(), "Profile2.prof")
s2 = pstats.Stats("Profile2.prof")
s2.strip_dirs().sort_stats("time").print_stats()


'''
# Raw Python
Sun Dec 16 12:35:46 2018    Profile0.prof

         7000004 function calls in 11.474 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1000000    7.348    0.000   10.312    0.000 great_circle_v0.py:11(great_circle)
  3000000    1.501    0.000    1.501    0.000 {built-in method math.cos}
        1    1.161    1.161   11.474   11.474 great_circle_v0.py:20(great_circle_loop)
  2000000    0.995    0.000    0.995    0.000 {built-in method math.sin}
  1000000    0.469    0.000    0.469    0.000 {built-in method math.acos}
        1    0.000    0.000   11.474   11.474 {built-in method builtins.exec}
        1    0.000    0.000   11.474   11.474 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


# CPython
Sun Dec 16 12:35:51 2018    Profile1.prof

         4 function calls in 5.175 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    5.174    5.174    5.174    5.174 {great_circle_v1.great_circle_loop}
        1    0.000    0.000    5.175    5.175 {built-in method builtins.exec}
        1    0.000    0.000    5.174    5.174 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


# No Python
Sun Dec 16 12:35:52 2018    Profile2.prof

         4 function calls in 0.787 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.787    0.787    0.787    0.787 {great_circle_v2.great_circle_loop}
        1    0.000    0.000    0.787    0.787 {built-in method builtins.exec}
        1    0.000    0.000    0.787    0.787 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
'''