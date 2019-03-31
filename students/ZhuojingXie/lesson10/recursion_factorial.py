
import time

def factorial(n):
    if n <= 0:
        return
    elif n == 1:
        return n
    else:
        return n * factorial(n - 1)




def factorial_v1(n):
    if n<=0:
        return
    elif n == 1:
        return 1
    else:
        num = 1
        while n >1:
            num = num * n
            n = n - 1
        return num


if __name__ == "__main__":
    st = time.clock()
    for i in range(1000000):
        result = factorial(60)
    print(f"No recursion time for Fibonacci: {time.clock() - st}")


    st = time.clock()
    for i in range(1000000):
        result = factorial_v1(60)
    print(f"recursion time for Fibonacci: {time.clock() - st}")
