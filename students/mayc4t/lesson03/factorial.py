#!/usr/bin/env python3

import math
COUNT=10

def recursive_factorial(n):
    """Calculate the factorial value of a number, recursively.

    Args:
      n: Value to compute the factorial for. Type: integer
    """
    if n == 0 or n == 1:
        return 1
    return (n * recursive_factorial( n-1))

# Simple loop to test recursive_factorial function.
for idx in range(COUNT):
    ans = math.factorial(idx)
    print('factorial({idx}) = {ans}'.format(
        idx=idx,
        ans=ans))
    assert(ans == recursive_factorial(idx))
