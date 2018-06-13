
def intsum(current=0, next_i=0):
    """ 
    Adds the next integer to current int.

    0 + 1 + 2 + 3 + 4 + 5 + …
    --> 0, 1, 3, 6, 10, 15 …..
    """
    while True:
        current += next_i
        next_i += 1
        yield current       


def doubler(number=1):
    """ 
    Current is double the previous value.
    --> 1, 2, 4, 8, 16, 32,
    """
    while True:
        yield number
        number *= 2


def fib(prev_i=0, next_i=1):
    """
    f(n) = f(n-1) + f(n-2)
    --> 1, 1, 2, 3, 5, 8, 13, 21, 34…
    """
    while True:
        fib_i = next_i
        yield fib_i

        # Fib num becomes combination of 1st and 2nd nums in sequence.  Those get incremented to the next in sequence.
        fib_i = prev_i + next_i
        prev_i = next_i
        next_i = fib_i
    

def prime(number=2):
    """
    Generates prime numbers.
    2, 3, 5, 7, 11, 13, 17, 19, 23…
    """
    while True:
        if number < 2 or not [x for x in range(2, number) if number % x == 0]:
            yield number
        number += 1

def count_threes(number=0):
    """Counts by 3s. """
    while True:
        yield number
        number += 3