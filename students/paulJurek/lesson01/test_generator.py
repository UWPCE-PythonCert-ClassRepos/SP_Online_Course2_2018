"""test to make sure generators have the right behavior"""

import generator_assignment as gm


def test_generate_increasing_ints():
    """tests generator works for 5 iterations and sums results"""
    gen = gm.generate_increasing_ints(start=0, step=1)

    assert next(gen) == 0
    assert next(gen) == 1
    assert next(gen) == 3
    assert next(gen) == 6
    assert next(gen) == 10
    assert next(gen) == 15
    
def test_doubler():
    """tests generator works for 5 iterations and doubles results"""
    doubler = gm.Doubler(start=1, step=2)

    assert next(doubler) == 1
    assert next(doubler) == 2
    assert next(doubler) == 4
    assert next(doubler) == 8
    assert next(doubler) == 16
    assert next(doubler) == 32

def test_fibonacci():
    """given Fibonacci generator
    when next is called
    the correct values is returned""" 

    fib = gm.Fibonacci()

    assert next(fib) == 1
    assert next(fib) == 1
    assert next(fib) == 2
    assert next(fib) == 3
    assert next(fib) == 5
    assert next(fib) == 8
    assert next(fib) == 13
    assert next(fib) == 21
 
def test_primes():
    """test prime number generator identifies prime numbers correctly"""
    gen = gm.primes()

    assert next(gen) == 2
    assert next(gen) == 3
    assert next(gen) == 5
    assert next(gen) == 7
    assert next(gen) == 11
    assert next(gen) == 13
    assert next(gen) == 17
    assert next(gen) == 19
    assert next(gen) == 23
