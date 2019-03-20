#-------------------------------------------------#
# Title: Recursion - Factorial
# Dev:   LDenney
# Date:  February 13th, 2019
# ChangeLog: (Who, When, What)
#   Laura Denney, 2/13/19, Started work on recursion assignment
#-------------------------------------------------#

def factorial(n):
    if n == 1:
        return n
    else:
        return n * factorial(n-1)
