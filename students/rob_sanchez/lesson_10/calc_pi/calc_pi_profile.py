#!/usr/bin/env python3

import pstats
import cProfile
import calc_pi

import pyximport
pyximport.install()


cProfile.runctx("calc_pi.approx_pi()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()
