'''
Shin Tran
Python 220
Assignment 10

Explore code-only performance improvement strategies such as memoization
'''

import time


def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)


fib_memo = {}
def fib_m(n):
    if n < 2:
        return n
    if n not in fib_memo:
        fib_memo[n] = fib_m(n-1) + fib_m(n-2)
    return fib_memo[n]


if __name__ == "__main__":
    itr_start = 30
    itr_end = 35

    start1 = time.time()
    for i in range(itr_start, itr_end):
        print("When i is {} then: {}".format(i, fib_m(i)))
    print("Process took {:.10f} seconds.".format(time.time() - start1))
    print()

    start2 = time.time()
    for j in range(itr_start, itr_end):
        print("When j is {} then: {}".format(j, fib(j)))
    print("Process took {:.10f} seconds.".format(time.time() - start2))

'''
$ python memoization.py
When i is 30 then: 832040
When i is 31 then: 1346269
When i is 32 then: 2178309
When i is 33 then: 3524578
When i is 34 then: 5702887
Process took 0.0000000000 seconds.

When j is 30 then: 832040
When j is 31 then: 1346269
When j is 32 then: 2178309
When j is 33 then: 3524578
When j is 34 then: 5702887
Process took 7.7966341972 seconds.
'''