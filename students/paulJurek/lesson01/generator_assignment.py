"""creates numerous generators as part of Python 220, lesson01"""

def generate_increasing_ints(start: int=0, step: int=1):
    """keep adding the next integer
    0 + 1 + 2 + 3 + 4 + 5 + …"""
    current_num = step
    current_total = start

    while True:
        yield current_total
        current_total += current_num
        current_num += 1

def Doubler(start: int=1, step: int=2):
    """keeps doubling previous value
    args:
        start: strting int.  Must be non-zero
        step: indicates multiple each iteration increases value by"""
    current_num = start

    while True:
        yield current_num
        current_num *= step

def Fibonacci():
    """runs fibonacci series.  User can modify starting position if needed
    args:
        start: strting int.  Must be non-zero"""

    yield 1
    previous_num = 0
    current_num = 1    

    while True:
            previous_num, current_num = current_num, previous_num + current_num
            yield current_num

def primes():
        """creates a prime number generator starting at 2"""
        prime = 2

        while True:
                divs = []
                divs = [x for x in range(1,prime//2+1) if prime % x==0]
                if len(divs)==1:
                        yield prime
                prime += 1
