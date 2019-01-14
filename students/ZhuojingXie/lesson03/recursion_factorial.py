
def factorial(n):
    if n <= 0:
        return
    elif n == 1:
        return n
    else:
        return n * factorial(n - 1)
