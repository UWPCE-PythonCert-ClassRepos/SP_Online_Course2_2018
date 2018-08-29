#Lesson 05 Practice Exercise to submit

#recursive.py

#this function should take the number n and return either true or false.


import sys

def my_fun(n):
    #if n < 1:
        #return False

    if n == 2:
        return True

    return my_fun(n/2)

if __name__ == '__main__':
    n = int(sys.argv[1])
    print(my_fun(n))

#what are some other values of n that will return true? 8, 16, 32, 64, 128
#What is the general rule? N is a power of 2.
#what kind of numbers will this function return true for? powers of 2.

#a recursion error means the function keeps calling itself repeatedly

#use the debugger using an n of 15.

#there is no else for the 'if' statement, so rather than returning false, it
#continues to run the recursion until it reaches the max number of recursions.




