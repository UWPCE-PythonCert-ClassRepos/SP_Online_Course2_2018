import time


def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper

@memoize
def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

def fib1(n):
    if n <= 1:
        return n
    else:
        return fib1(n-1) + fib1(n-2)



if __name__ == '__main__':
    start = time.time()
    print(fib(35))
    print("Memoized implemematation: " + str(time.time() - start))

    start = time.time()
    print(fib1(35))
    print("Regualr recursive implemematation: " + str(time.time() - start))

    init = time.clock()
    print(fib(35))
    print("Using clock: " + str(time.clock() - init))




