#!/usr/bin/env python3
#Lesson 3: Recursive Factorial

def factorial(n=0):
    if n <= 1:
        return 1
    return n*factorial(n-1)

if __name__ == '__main__':
    fact_list = [factorial(i) for i in range(20)]
    for i in range(len(fact_list)):
        print(i, "=" ,fact_list[i])