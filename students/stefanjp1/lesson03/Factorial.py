
def factorial(n):
    if n < 0 or not isinstance(n, int):
        raise ValueError('n must be a non-negative intiger')
    
    if n == 0:
        return 1
    else:
        return factorial(n-1) * n

if __name__ == "__main__":
    print('9 Factorial: {}'.format(factorial(9)))
    print('5 Factorial: {}'.format(factorial(5)))
    print('1 Factorial: {}'.format(factorial(1)))
    print('0 Factorial: {}'.format(factorial(0)))