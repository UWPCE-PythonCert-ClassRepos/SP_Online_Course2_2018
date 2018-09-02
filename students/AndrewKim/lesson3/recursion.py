#!/usr/bin/env python3

def factorial(n):
    if n <= 1:
        return 1
    else:
        return factorial(n-1) * n

        
if __name__ == "__main__":
    for i in range(0, 10):
        print("{}: {}".format(i, factorial(i)))