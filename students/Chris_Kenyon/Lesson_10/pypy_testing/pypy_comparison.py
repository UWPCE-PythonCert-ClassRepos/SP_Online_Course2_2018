import utilities
from configparser import ConfigParser
import logging
import time
from math import sqrt, factorial

log = utilities.configure_logger('default', '../logs/pypy_factorial.log')
log.info('Running series generators from python environment')

def factorial(n=0):
    """
    Recursive factorial series
    """
    if n <= 1:
        return 1
    return n*factorial(n-1)

def lucas(n):
    """
    Non Recursive Lucas Series from 210 class exercise
    """
    if n > 0:
        # create array of zeros with size n
        lucser = [0] * n
        # set initial values
        lucser[0] = 2
        if n > 1:
            lucser[1] = 1
        # create full fibonacci sequence
        for i in range(2, n):
            lucser[i] = lucser[i-2] + lucser[i-1]
        # print specified nth value (n-1 due to index starting at 0)
        return(lucser[n-1])
    else:
        print("Please select an integer greater than 1")
        
def fibonacci(n):
    """
    Recursiive Fibonacci Sequence
    """
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)


if __name__ == "__main__":
    
    n = 35

    init = time.clock()
    print([fibonacci(n)])
    log.info(f"Runtime for Fibonacci function, n = {n}: {time.clock() - init}")

    init = time.clock()
    print([factorial(i) for i in range(n)])
    log.info(f"Runtime for factorial function, n = {n}: {time.clock() - init}")

    init = time.clock()
    print([lucas(i) for i in range(n)])
    log.info(f"Runtime for lucas function, n = {n}: {time.clock() - init}")