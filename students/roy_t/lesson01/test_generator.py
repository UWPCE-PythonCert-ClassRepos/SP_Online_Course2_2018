#!/usr/bin/env python3

__author__ = "Roy Tate - githubtater"


def sum_of_integers(nums):
    """Keep adding the next integer in the list"""
    sum_num = 0
    for i in nums:
        sum_num += i
        try:
            yield nums[i+1] + sum_num
        except IndexError as e:
            pass


def doubler(nums):
    """Each value is double the previous value"""
    val = nums[1]
    for i in nums:
        yield val
        val += val

def fibonacci_sequence(n):
    """Return the fibonacci series of length n."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def prime_numbers(n):
    """Generate the prime numbers"""
    for cur_num in nums:
        under_slice = nums[:cur_num]
        count = 0
        for index in len(under_slice):
            count += 1
            try:
                if cur_num % index != 0:
                    yield
            except ZeroDivisionError as e:
                continue
            yield cur_num



nums = range(10)
sums = sum_of_integers(nums)
doubs = doubler(nums)
fibs = fibonacci_sequence(10)
prims = prime_numbers(nums)

for num in prims:
    print(num)
