

# implements a recursive factorial function
def factorial(n):
    return 1 if (n < 1) else n * factorial(n-1)

print(factorial(0))
print(factorial(5))
print(factorial(10))
print(factorial(15))
