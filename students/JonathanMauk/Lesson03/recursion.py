def factorial(n):
    """Returns the factorial of a given non-negative integer,
    the product of all positive integers less than or equal to that number."""
    if n != int:
        print("Please enter an integer.")
    elif n < 0:
        print("Please enter a non-negative integer.")
    elif n == 0 or n == 1:
        return 1
