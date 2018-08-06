from some_module import *
from timeit import timeit as timer

print(hewwo())

print(timer(lambda: run_fact()))

print(timer(lambda: run_fibo()))

print(timer(lambda: alt_run_fibo()))
