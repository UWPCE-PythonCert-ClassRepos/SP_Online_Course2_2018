def recur_fibo(n):
    """Recursive function to
    print Fibonacci sequence"""
    if n <= 1:
        return n
    else:
        return recur_fibo(n-1) + recur_fibo(n-2)


x = recur_fibo(40)