'''
Shin Tran
Python 220
Assignment 10

Explore/demo Python’s memory_profiler. https://pypi.python.org/pypi/memory_profiler
'''


@profile
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)

fib_memo = {}
@profile
def fib_m(n):
    if n < 2:
        return n
    if n not in fib_memo:
        fib_memo[n] = fib_m(n-1) + fib_m(n-2)
    return fib_memo[n]


if __name__ == "__main__":
    itr_start = 15
    itr_end = 20

    for i in range(itr_start, itr_end):
        print("When i is {} then: {}".format(i, fib_m(i)))
    print()

    for j in range(itr_start, itr_end):
        print("When j is {} then: {}".format(j, fib(j)))


'''
Output:
$ python -m memory_profiler mem_profiler_ex.py
When i is 15 then: 610
When i is 16 then: 987
When i is 17 then: 1597
When i is 18 then: 2584
When i is 19 then: 4181

When j is 15 then: 610
When j is 16 then: 987
When j is 17 then: 1597
When j is 18 then: 2584
When j is 19 then: 4181
Filename: mem_profiler_ex.py

Line #    Mem usage    Increment   Line Contents
================================================
    10   32.020 MiB   32.020 MiB   @profile
    11                             def fib(n):
    12   32.020 MiB    0.000 MiB       if n < 2:
    13   32.020 MiB    0.000 MiB           return n
    14                                 else:
    15   32.020 MiB    0.000 MiB           return fib(n-1) + fib(n-2)


Filename: mem_profiler_ex.py

Line #    Mem usage    Increment   Line Contents
================================================
    18   32.020 MiB   32.020 MiB   @profile
    19                             def fib_m(n):
    20   32.020 MiB    0.000 MiB       if n < 2:
    21   32.020 MiB    0.000 MiB           return n
    22   32.020 MiB    0.000 MiB       if n not in fib_memo:
    23   32.020 MiB    0.000 MiB           fib_memo[n] = fib_m(n-1) + fib_m(n-2)
    24   32.020 MiB    0.000 MiB       return fib_memo[n]
'''
