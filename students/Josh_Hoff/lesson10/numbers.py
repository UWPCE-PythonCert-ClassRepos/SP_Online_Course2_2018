from memory_profiler import profile

@profile
def Fibonacci(x=7):
    num1 = 1
    num2 = 2
    sequence = f'{num1}, {num2}'
    
    for i in range(1, x):
        nextnum = num1 + num2
        sequence = f'{sequence}, {nextnum}'
        num1 = num2
        num2 = nextnum
    return nextnum

@profile
def Triangular(x=7):
    start = 0
    
    sequence = f'{start}'
    nextnum = start
    
    for i in range(1, x):
        nextnum += i
        sequence = f'{sequence}, {nextnum}'
    return nextnum

@profile
def Test(n=100):
    numbers = [ i**2 for i in range(n)]
    return numbers
        