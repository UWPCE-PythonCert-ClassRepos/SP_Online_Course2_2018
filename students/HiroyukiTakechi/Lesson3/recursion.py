'''
Lesson 3 Assignment #2
Recursive

'''

def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)

print(fact(5))

