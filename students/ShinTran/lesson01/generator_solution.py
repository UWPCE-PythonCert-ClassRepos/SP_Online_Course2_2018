'''
Shin Tran
Python 220
Lesson 1 Assignment
'''


class intsum():
    # Sum of the intergers
    # 0,1,3,6,10,15,...
    def __init__(self):
        self._num = 0
        self._sum = 0

    def __iter__(self):
        return self

    def __next__(self):
        self._sum += self._num
        self._num = self._num + 1
        return self._sum


class doubler():
    # Doubles the previous value (exponents of 2)
    # 1,2,4,8,16,32,...
    def __init__(self):
        self._num = -1

    def __iter__(self):
        return self

    def __next__(self):
        self._num += 1
        return 2 ** self._num


class fib():
    # Fibonacci sequence
    # 1,1,2,3,5,8,13,21,34,...
    def __init__(self):
        self._num1 = 0
        self._num2 = 1

    def __iter__(self):
        return self

    def __next__(self):
        ret_val = self._num2
        self._num2 += self._num1
        self._num1 = ret_val
        return ret_val

class prime():
    # Prime Numbers sequence
    # 2, 3, 5, 7, 11, 13, 17, 19, 23,...
    def __init__(self):
        self._num = 1

    def __iter__(self):
        return self

    def __next__(self):
        ret_val = self.iterate_n()
        return ret_val

    def iterate_n(self):
        self._num += 1
        while not self.is_prime():
            self.iterate_n()
        return self._num

    def is_prime(self):
        for x in range(2, self._num):
            if self._num % x == 0:
                return False
        return True

'''
if __name__ == "__main__":
    
    sum1 = intsum()
    for i in range(5):
        print(next(sum1))

    dblr = doubler()
    for j in range(5):
        print(next(dblr))
    
    fibo = fib()
    for k in range(10):
        print(next(fibo))
    
    prim = prime()
    for l in range(10):
        print(next(prim))
'''