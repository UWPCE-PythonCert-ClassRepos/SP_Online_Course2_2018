import generator as gen

def test_sum():
    n = gen.sum()

    assert next(n) == 0
    assert next(n) == 1
    assert next(n) == 3
    assert next(n) == 6

def test_doubler():
    n = gen.doubler()
    assert next(n) == 1
    assert next(n) == 2
    assert next(n) == 4
    assert next(n) == 8

def test_fibonacci():
    n = gen.fibonacci()
    assert [next(n) for i in range(9)] == [1, 1, 2, 3, 5, 8, 13, 21, 34]

def test_prime():
    n = gen.prime()
    for val in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        assert next(n) == val


