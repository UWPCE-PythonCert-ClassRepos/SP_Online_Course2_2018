# memory profiler exercise
# from http://perfectresolution.com/2016/10/use-the-python-memory-profiler/

import random

@profile
def memory_test():
    numbers = [random.randint(0, 1000) for x in range (100000)]
    biggest = max(numbers)
    return biggest

memory_test()

""" python -m memory_profiler output:

Filename: memprof_test.py

Line #    Mem usage    Increment   Line Contents
================================================
     6   32.414 MiB   32.414 MiB   @profile
     7                             def memory_test():
     8   36.805 MiB    0.703 MiB       numbers = [random.randint(0, 1000) for x in range (100000)]
     9   36.805 MiB    0.000 MiB       biggest = max(numbers)
    10   36.805 MiB    0.000 MiB       return biggest

"""

""" python -m cProfile output  (removed frozen importlib, built in,
    and method lines for readability):


         503672 function calls (503629 primitive calls) in 0.266 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 bisect.py:1(<module>)
       14    0.000    0.000    0.000    0.000 hashlib.py:116(__get_openssl_constructor)
        1    0.000    0.000    0.003    0.003 hashlib.py:54(<module>)
        8    0.000    0.000    0.000    0.000 hashlib.py:73(__get_builtin_constructor)
        1    0.002    0.002    0.266    0.266 memprof_test.py:4(<module>)
        1    0.000    0.000    0.257    0.257 memprof_test.py:7(memory_test)
        1    0.032    0.032    0.254    0.254 memprof_test.py:8(<listcomp>)
   100000    0.093    0.000    0.181    0.000 random.py:173(randrange)
   100000    0.040    0.000    0.221    0.000 random.py:217(randint)
   100000    0.061    0.000    0.088    0.000 random.py:223(_randbelow)
        1    0.000    0.000    0.005    0.005 random.py:38(<module>)
        1    0.000    0.000    0.000    0.000 random.py:664(SystemRandom)
        1    0.000    0.000    0.000    0.000 random.py:71(Random)
        1    0.000    0.000    0.000    0.000 random.py:87(__init__)
        1    0.000    0.000    0.000    0.000 random.py:96(seed)
        """

