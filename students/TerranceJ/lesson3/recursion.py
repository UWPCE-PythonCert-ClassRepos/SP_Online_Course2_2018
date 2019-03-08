"""
Lesson 3 Recursion Assignment
Terrance J
March 2, 2019
"""

def factorial(n):
    if n == 1:
        return 1

    elif n < 1:
        raise ValueError("Number must be greater than 1")
    
    else:
        return n * factorial(n-1)


if __name__ == '__main__':  
    print(factorial(5))    
    print(factorial(10))
    

    

