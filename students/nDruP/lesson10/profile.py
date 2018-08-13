# profile.py

import pstats, cProfile

import pyximport
pyximport.install()

from some_module import *

cProfile.runctx("run_fact()", globals(), locals(), "Profile.prof")

cProfile.runctx("run_fibo()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()
