"""
Recursive factorial function
- 5! --> 5 * 4 * 3 * 2 * 1
- 1! & 0! = 1
"""

def factorial(num):
    if num <= 1:
        return 1
    else:
        return num * factorial(num-1)


if __name__ == "__main__":
    for x in range(0, 15):
        print(f"Factorial for {x} is {factorial(x)}")

    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6

    assert factorial(10) == 3628800