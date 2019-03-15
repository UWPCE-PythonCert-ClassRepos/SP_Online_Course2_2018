import math
import time
#Using Python3 and Pypy to measure performance.


def factorial(n):
    """Return the product of all positive integers less than or equal to n"""
    if n <= 0:
        return 1
    else:
        return n * factorial(n-1)


def lucas(n):
    """Return the nth value in the Lucas series"""
    if n == 0:
        return 2
    elif n == 1:
        return 1
    else:
        return lucas(n-2) + lucas(n-1)


if __name__ == '__main__':
    init = time.clock()
   
    for n in range(30):
        value = factorial(n)
        print('If n equals {}, the value of the factorial is {} '.format(n, value))
    print('Factorial series took: {}'.format(time.clock() - init))
   
    init_two = time.clock()
    for n in range(30):
        value = lucas(n)
        print('If n equals {}, the value of the lucas series is {} '.format(n, value))
    print('Lucas series took: {}'.format(time.clock() - init_two))
    

# OUTPUT WITH PYTHON 3.6

# If n equals 0, the value of the factorial is 1
# If n equals 1, the value of the factorial is 1
# If n equals 2, the value of the factorial is 2
# If n equals 3, the value of the factorial is 6
# If n equals 4, the value of the factorial is 24
# If n equals 5, the value of the factorial is 120
# If n equals 6, the value of the factorial is 720
# If n equals 7, the value of the factorial is 5040
# If n equals 8, the value of the factorial is 40320
# If n equals 9, the value of the factorial is 362880
# If n equals 10, the value of the factorial is 3628800
# If n equals 11, the value of the factorial is 39916800
# If n equals 12, the value of the factorial is 479001600
# If n equals 13, the value of the factorial is 6227020800
# If n equals 14, the value of the factorial is 87178291200
# If n equals 15, the value of the factorial is 1307674368000
# If n equals 16, the value of the factorial is 20922789888000
# If n equals 17, the value of the factorial is 355687428096000
# If n equals 18, the value of the factorial is 6402373705728000
# If n equals 19, the value of the factorial is 121645100408832000
# If n equals 20, the value of the factorial is 2432902008176640000
# If n equals 21, the value of the factorial is 51090942171709440000
# If n equals 22, the value of the factorial is 1124000727777607680000
# If n equals 23, the value of the factorial is 25852016738884976640000
# If n equals 24, the value of the factorial is 620448401733239439360000
# If n equals 25, the value of the factorial is 15511210043330985984000000
# If n equals 26, the value of the factorial is 403291461126605635584000000
# If n equals 27, the value of the factorial is 10888869450418352160768000000
# If n equals 28, the value of the factorial is 304888344611713860501504000000
# If n equals 29, the value of the factorial is 8841761993739701954543616000000
# Factorial series took: 0.03734865979028754
# If n equals 0, the value of the lucas series is 2
# If n equals 1, the value of the lucas series is 1
# If n equals 2, the value of the lucas series is 3
# If n equals 3, the value of the lucas series is 4
# If n equals 4, the value of the lucas series is 7
# If n equals 5, the value of the lucas series is 11
# If n equals 6, the value of the lucas series is 18
# If n equals 7, the value of the lucas series is 29
# If n equals 8, the value of the lucas series is 47
# If n equals 9, the value of the lucas series is 76
# If n equals 10, the value of the lucas series is 123
# If n equals 11, the value of the lucas series is 199
# If n equals 12, the value of the lucas series is 322
# If n equals 13, the value of the lucas series is 521
# If n equals 14, the value of the lucas series is 843
# If n equals 15, the value of the lucas series is 1364
# If n equals 16, the value of the lucas series is 2207
# If n equals 17, the value of the lucas series is 3571
# If n equals 18, the value of the lucas series is 5778
# If n equals 19, the value of the lucas series is 9349
# If n equals 20, the value of the lucas series is 15127
# If n equals 21, the value of the lucas series is 24476
# If n equals 22, the value of the lucas series is 39603
# If n equals 23, the value of the lucas series is 64079
# If n equals 24, the value of the lucas series is 103682
# If n equals 25, the value of the lucas series is 167761
# If n equals 26, the value of the lucas series is 271443
# If n equals 27, the value of the lucas series is 439204
# If n equals 28, the value of the lucas series is 710647
# If n equals 29, the value of the lucas series is 1149851
# Lucas series took: 2.863000632900566

# OUTPUT WITH PYPY3

# If n equals 0, the value of the factorial is 1
# If n equals 1, the value of the factorial is 1
# If n equals 2, the value of the factorial is 2
# If n equals 3, the value of the factorial is 6
# If n equals 4, the value of the factorial is 24
# If n equals 5, the value of the factorial is 120
# If n equals 6, the value of the factorial is 720
# If n equals 7, the value of the factorial is 5040
# If n equals 8, the value of the factorial is 40320
# If n equals 9, the value of the factorial is 362880
# If n equals 10, the value of the factorial is 3628800
# If n equals 11, the value of the factorial is 39916800
# If n equals 12, the value of the factorial is 479001600
# If n equals 13, the value of the factorial is 6227020800
# If n equals 14, the value of the factorial is 87178291200
# If n equals 15, the value of the factorial is 1307674368000
# If n equals 16, the value of the factorial is 20922789888000
# If n equals 17, the value of the factorial is 355687428096000
# If n equals 18, the value of the factorial is 6402373705728000
# If n equals 19, the value of the factorial is 121645100408832000
# If n equals 20, the value of the factorial is 2432902008176640000
# If n equals 21, the value of the factorial is 51090942171709440000
# If n equals 22, the value of the factorial is 1124000727777607680000
# If n equals 23, the value of the factorial is 25852016738884976640000
# If n equals 24, the value of the factorial is 620448401733239439360000
# If n equals 25, the value of the factorial is 15511210043330985984000000
# If n equals 26, the value of the factorial is 403291461126605635584000000
# If n equals 27, the value of the factorial is 10888869450418352160768000000
# If n equals 28, the value of the factorial is 304888344611713860501504000000
# If n equals 29, the value of the factorial is 8841761993739701954543616000000
# Factorial series took: 0.13192726775115035
# If n equals 0, the value of the lucas series is 2
# If n equals 1, the value of the lucas series is 1
# If n equals 2, the value of the lucas series is 3
# If n equals 3, the value of the lucas series is 4
# If n equals 4, the value of the lucas series is 7
# If n equals 5, the value of the lucas series is 11
# If n equals 6, the value of the lucas series is 18
# If n equals 7, the value of the lucas series is 29
# If n equals 8, the value of the lucas series is 47
# If n equals 9, the value of the lucas series is 76
# If n equals 10, the value of the lucas series is 123
# If n equals 11, the value of the lucas series is 199
# If n equals 12, the value of the lucas series is 322
# If n equals 13, the value of the lucas series is 521
# If n equals 14, the value of the lucas series is 843
# If n equals 15, the value of the lucas series is 1364
# If n equals 16, the value of the lucas series is 2207
# If n equals 17, the value of the lucas series is 3571
# If n equals 18, the value of the lucas series is 5778
# If n equals 19, the value of the lucas series is 9349
# If n equals 20, the value of the lucas series is 15127
# If n equals 21, the value of the lucas series is 24476
# If n equals 22, the value of the lucas series is 39603
# If n equals 23, the value of the lucas series is 64079
# If n equals 24, the value of the lucas series is 103682
# If n equals 25, the value of the lucas series is 167761
# If n equals 26, the value of the lucas series is 271443
# If n equals 27, the value of the lucas series is 439204
# If n equals 28, the value of the lucas series is 710647
# If n equals 29, the value of the lucas series is 1149851
# Lucas series took: 0.3748372419219651
