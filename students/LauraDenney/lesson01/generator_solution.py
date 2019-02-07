#-------------------------------------------------#
# Title: Generator Exercise
# Dev:   LDenney
# Date:  February 3rd, 2019
# ChangeLog: (Who, When, What)
#   Laura Denney, 2/3/19, Started work on Generator Exercise
#-------------------------------------------------#

#generator_solution

def intsum():
    num = 0
    n = 0
    while True:
        yield num
        n +=1
        num += n



def intsum2():
    num = 0
    n = 0
    while True:
        yield num
        n +=1
        num += n

def doubler():
    num = 1
    while True:
        yield num
        num*=2

def fib():
    n = 0
    num = 1
    while True:
        yield num
        num_temp = num
        num = n + num
        n = num_temp

def prime():
    num = 2
    list_num = [2,3,5,7]
    while True:
        if num in list_num:
            yield num
        elif (num%2 and num%3 and num%5 and num%7):
            yield num
        num +=1