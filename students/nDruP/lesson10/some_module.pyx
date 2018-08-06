def fibonacci(n):
    if n < 2:
       return 1
    return fibonacci(n-1)+fibonacci(n-2)

def hewwo():
    print('H-hewwo world?!')

def factorial(n):
    if n <= 1:
       return 1
    return n * factorial(n-1)