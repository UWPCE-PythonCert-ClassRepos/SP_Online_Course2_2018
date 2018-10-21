'''
Shin Tran
Python 220
Lesson 3 Assignment
'''

# A recursive solution for the factorial function


def factorial(num):
    if num < 1:
        return 1
    else:
        return num * factorial(num - 1)

if __name__ == "__main__":
    for i in range(3, 10):
        print("Factorial of {} is {}.".format(i, factorial(i)))

