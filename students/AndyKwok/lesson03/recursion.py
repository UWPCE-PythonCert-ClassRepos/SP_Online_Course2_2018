# Author: Andy Kwok
# Last Updated: 11/11/18

#!/usr/bin/env python3

def factorial (n):
    if n > 0: return n * factorial(n-1)
    if n == 0: return 1
    if n < 0:
        print("Negative Numbers do not have factorials!")

if __name__ == "__main__":
    assert(factorial(5) == 120)
    assert(factorial(8) == 40320)
    assert(factorial(10) == 3628800)
    assert(factorial(13) == 6227020800)
    print("No errors are encountered...")