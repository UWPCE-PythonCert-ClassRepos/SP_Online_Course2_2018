'''
Shin Tran
Python 220
Assignment 10

Explore/demo cProfile side by side with PyCharm’s built-in profilers
'''

from timeit import timeit as timer
import cProfile
import re

reps = 7500
my_range = 7500
lower_lim = my_range / 2
my_list = list(range(my_range))


def mult_by_two(x):
    return x * 2


def gtr_than_low_lim(x):
    return x > lower_lim

'''
print("map filter with functions")
print(timer(
    'map(mult_by_two, filter(gtr_than_low_lim, my_list))',
    globals = globals(), number = reps))
print("map filter with lambdas")
print(timer(
    'map(lambda x: x * 2, filter(lambda x: x > lower_lim, my_list))',
    globals = globals(), number = reps))
print("comprehension")
print(timer(
    '[x * 2 for x in my_list if x > lower_lim]',
    globals = globals(), number = reps))
print("comprehension with functions")
print(timer(
    '[mult_by_two(x) for x in my_list if gtr_than_low_lim(x)]',
    globals = globals(), number = reps))
print("comprehension with lambdas")
print(timer(
    '[(lambda x: x * 2)(x) for x in my_list if (lambda x: x > lower_lim)(x)]',
    globals = globals(), number = reps))
'''

print("map filter with functions")
cProfile.run('re.compile("map(mult_by_two, filter(gtr_than_low_lim, my_list))")')

print("map filter with lambdas")
cProfile.run('re.compile("map(lambda x: x * 2, filter(lambda x: x > lower_lim, my_list))")')

print("comprehension")
cProfile.run('re.compile("[x * 2 for x in my_list if x > lower_lim]")')

print("comprehension with functions")
cProfile.run('re.compile("[mult_by_two(x) for x in my_list if gtr_than_low_lim(x)]")')

print("comprehension with lambdas")
cProfile.run('re.compile("[(lambda x: x * 2)(x) for x in my_list if (lambda x: x > lower_lim)(x)]")')
