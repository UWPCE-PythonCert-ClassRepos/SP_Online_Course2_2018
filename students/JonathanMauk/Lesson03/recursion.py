def factorial(n):
    """Returns the factorial of a given non-negative integer,
    the product of all positive integers less than or equal to that number."""
    if n == float:
        print(f"Please enter an integer. You entered {n}.")
        return
    elif n < 0:
        print(f"Please enter a non-negative integer. You entered {n}.")
        return
    elif n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


if __name__ == "__main__":
    print("The factorial of 0 is: " + str(factorial(0)))  # Should be 1.
    print("The factorial of 1 is: " + str(factorial(1)))  # Should also be 1.
    print("The factorial of 3 is: " + str(factorial(3)))  # Should also be 6.
    print("The factorial of 8 is: " + str(factorial(8)))  # Should also be 40,320.
