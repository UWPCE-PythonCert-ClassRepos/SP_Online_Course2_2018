#!/usr/bin/env python3

def fact(n):
    if n == 0:
        return 1
    return n*fact(n-1)

if __name__ == "__main__":
    f = fact(0)
    assert f == 1

    f = fact(5)
    assert f == 120

    f = fact(7)
    assert f == 5040
