# cython: profile=True

def fibonacci(int n):
    if n < 2:
       return 1
    return fibonacci(n-1)+fibonacci(n-2)

def alt_fibonacci(n):
    cdef int two_fibo[2]
    two_fibo[:] = [1,1]
    for i in range(n-2):
        two_fibo[1] += two_fibo[0]
        two_fibo[0] = two_fibo[1] - two_fibo[0]
    return two_fibo[1]	
    

def hewwo():
    return 'H-hewwo world?!'

def factorial(int n):
    if n <= 1:
       return 1
    return n * factorial(n-1)

def run_fact():
    results = []
    for i in range(25):
        results.append(factorial(i))
    return results

def run_fibo():
    results = []
    for i in range(15):
        results.append(fibonacci(i))
    return results

def alt_run_fibo():
    results = []
    for i in range(15):
        results.append(alt_fibonacci(i))
    return results