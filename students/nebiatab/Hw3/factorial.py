# Factorial

def factorial(x):
  if x == 1:
    return 1
  else:
    total = x * factorial(x-1)
    return total



print(factorial(5))