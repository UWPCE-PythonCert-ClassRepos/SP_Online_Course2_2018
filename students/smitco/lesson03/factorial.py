# lesson 03 factorial exercise
# !/usr/bin/env python3

def factorial(n):
    if n == 1:
        return 1
    else:
        return(n * factorial(n-1))

        
num = 4
print("{}! is {}.".format(num, factorial(num)))

num = 6
print("{}! is {}.".format(num, factorial(num)))

num = 1
print("{}! is {}.".format(num, factorial(num)))

num = 9
print("{}! is {}.".format(num, factorial(num)))