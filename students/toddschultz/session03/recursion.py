def rec(n):
    while n > 1:
        return n * rec(n-1)
    else:
        return 1

