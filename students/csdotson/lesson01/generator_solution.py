#!/usr/bin/env python
""" A series of simple generators """

def intsum():
    current = total = 0
    while True:
        yield(total)
        current += 1
        total += current


def doubler():
    total = 1
    while True:
        yield(total)
        total *= 2


def fib():
    n1, n2 = 0, 1
    while True:
        n1, n2 = n2, n1 + n2 
        yield (n1)



# def prime():
#     current = 2
#     divisor = [2]
#     while True:
#         for n in divisor:
#             if current % n:
#                 yield divisor
#                 divisor.append(current)
#             current += 1



#             # for num in divisor:
#             #     if current % num:
#             #         divisor.append(current)
#             #         yield current
#             #     current += 1




