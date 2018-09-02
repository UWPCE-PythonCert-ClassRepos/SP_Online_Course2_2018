#!/usr/bin/env python3

#Natalie Rodriguez
#UW Python - Course 2
#July 15, 2018
#Lesson 3 - Recursion


def recursion_fact(n):
   """Function to return the factorial
   of a number using recursion"""
   if n == 1:
       return n
   else:
       return n*recursion_fact(n-1)

# Change this value for a different result
#num = 7

num = int(input("Enter a number: "))

# check if the number is negative
if num < 0:
   print("Sorry, factorial does not exist for negative numbers")
elif num == 0:
   print("The factorial of 0 is 1")
else:
   print("The factorial of",num,"is",recursion_fact(num))

