#!/usr/bin/env python 3


def sum_of_int(max):
    '''Sum of the integers 0 + 1 + 2 + 3 + 4 + 5 + ...'''
    sum = 0
    a = 0
    while a < max:
        sum += a
        a += 1
        yield sum


def doubler(max):
    '''Each value is double the previous value: 1, 2, 4, 8, 16, 32, ...'''
    a = 1
    while a < max:
        yield a
        a *= 2


def fibo(input_number):
    '''Computes fibonacci numbers'''
    a = 0
    b = 1
    while b <= input_number:
        yield b
        temp = b
        b = a + b
        a = temp


def prime_numbers(input_number):
    '''Computes prime numbers, integers divisible only by 1 and itself.'''
    a = 2
    while a < input_number:
        for x in range(2, a):
            if a % x == 0:
                break
        else:
            yield a
        a += 1


def squared(max):
    '''Calculate the square of consecutive numbers'''
    a = 1
    while a < max:
        yield a * a
        a += 1


def cubed(max):
    '''Calculate the cube of consecutive numbers.'''
    a = 1
    while a < max:
        yield a * a * a
        a += 1


def counting_by(stop, counting_by_number):
    '''Counting by a number.'''
    if counting_by_number == 0:
        yield counting_by_number
    if counting_by_number > 0:
        a = 1
        while a < stop:
            yield a
            a += counting_by_number
    else:
        a = 1
        while a > stop:
            yield a
            a += counting_by_number


if __name__ == "__main__":

    print("Sum of consecutive integers: ")
    sums = sum_of_int(10)
    for x in sums:
        print(x)

    print("----------------------")
    print("Double last number: ")
    dbl = doubler(20)
    for x in dbl:
        print(x)

    print("----------------------")
    print("Fibonacci numbers")
    fib = fibo(30)
    for x in fib:
        print(x)

    print("----------------------")
    print("Prime numbers")
    prm = prime_numbers(30)
    for x in prm:
        print(x)

    print("----------------------")
    print("Squared numbers")
    sqred = squared(10)
    for x in sqred:
        print(x)

    print("----------------------")
    print("Cubed numbers")
    cbd = cubed(10)
    for x in cbd:
        print(x)

    print("----------------------")
    print("Generic function that counts by a number")
    print("----------------------")
    print("Count by 3")
    skip = counting_by(20, 3)
    for x in skip:
        print(x)
    print("----------------------")
    print("Count by 6")
    skip = counting_by(20, 6)
    for x in skip:
        print(x)
    print("----------------------")
    print("Count by -7")
    skip = counting_by(-40, -7)
    for x in skip:
        print(x)

