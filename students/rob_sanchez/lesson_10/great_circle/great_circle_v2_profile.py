#!/usr/bin/env python3

import pstats
import cProfile
import great_circle

import pyximport
pyximport.install()


cProfile.runctx("great_circle.run_test()",
                globals(), locals(), "great_circle_v2_Profile.prof")

s = pstats.Stats("great_circle_v2_Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()
