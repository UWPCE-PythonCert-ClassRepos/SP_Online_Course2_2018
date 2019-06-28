def sum_ints():
    """keep adding the next integer 0, 1, 2, 3, 4 = 0, 1, 3, 6, 10"""
    start = 0
    step = 1    
    current = step
    current_total = start

    while True:
        yield current_total
        current_total += current
        current += 1

def doubler():
    """double the value of the previous value"""
    start = 1

    while True:
        yield start
        start = start*2

def fib():
    """fibonacci sequence: f(n) = f(n-1) + f(n-2); 1, 1, 2, 3, 5, 8, 13, 21"""
    a, b = 1, 1
    while True:
        yield a
        a, b = b, b + a
                
def prime_num():
    """Generate the prime numbers (numbers only divisible by them self and 1):"""
    """2, 3, 5, 7, 11, 13, 17, 19, 23…"""
    a = 2
    while True:
        prime_list = [x for x in range(2,a) if a % x == 0]
        if len(prime_list) == 0:
            yield a
            a += 1
        else:
            a += 1



        



        
    
    

