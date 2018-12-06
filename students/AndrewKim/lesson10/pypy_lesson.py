import time
from math import sqrt, factorial

TIMES = 33

def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)



if __name__ == "__main__":

    init = time.clock()
    for i in range(TIMES):
        value = ((1+sqrt(5))**i-(1-sqrt(5))**i)/(2**i*sqrt(5))
    print "Fibonacci No function: " + str(time.clock() - init)

    init = time.clock()
    result = fib(TIMES)
    print "Fibonacci Function: " + str(time.clock() - init)

# Result of Python 2.7 interpretor
# andrew@andrew-VirtualBox:~/Desktop$ python pypy_lesson.py 
# Fibonacci No function: 0.000211
# Fibonacci Function: 3.089244

# Result of Pypy interpretor (much faster with function)
# andrew@andrew-VirtualBox:~/Desktop$ pypy pypy_lesson.py 
# Fibonacci No function: 0.000203839
# Fibonacci Function: 0.175470923

