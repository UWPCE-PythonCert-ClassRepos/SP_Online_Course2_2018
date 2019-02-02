"""implemenation of factorial with recursion"""

def factorial(n: int) -> int:
    """recursive implementation of factorial.  Simple example without error checking.
    args:
        n: positive integer for factoial input
    returns:
        integer of product of factorial"""
    # stop recursion when we get to 1
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

if __name__=="__main__":
    print(factorial(1))