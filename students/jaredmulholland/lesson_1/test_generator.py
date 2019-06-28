import sys
sys.path.append("C:\\Users\\Jared\\Documents\\python_220\\SP_Online_Course2_2018\\students\\jaredmulholland\\lesson_1")

from generator import sum_ints, doubler, fib, prime_num

def test_sum_ints():
    
    sum_ints_gen = sum_ints()
    sum_ints_list = []
    for _ in range(5):
        new_int = next(sum_ints_gen)
        sum_ints_list.append(new_int)

    assert sum_ints_list == [0,1,3,6,10]
        
def test_doubler():

    doubler_val = doubler()
    doubler_list = []

    for _ in range(7):
        new_doubler = next(doubler_val)
        doubler_list.append(new_doubler)

    assert doubler_list == [1,2,4,8,16,32,64]

def test_fib():
    
    fib_val = fib()
    fib_list = []

    for _ in range(7):
        new_fib = next(fib_val)
        fib_list.append(new_fib)

    assert fib_list == [1,1,2,3,5,8,13]

def test_prime_num():

    prime_val = prime_num()
    prime_list = []

    for _ in range(7):
        new_prime = next(prime_val)
        prime_list.append(new_prime)

    assert prime_list == [2,3,5,7,11,13,17]