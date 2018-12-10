# use recursion for factorial function!
# need termination condition
# define first step


def factorial_rec(num):
    if num == 1:
        return 1
    else:
        return num * factorial_rec(num - 1)
