# ----------------------------------------------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: factorial_recursion.py
# DATE CREATED: 9/30/2018
# UPDATED: 
# PURPOSE: Assignment 3, pt.2
# DESCRIPTION: The function finds the factorial (the product of all positive integers less than or equal to itself)
# by using recursion (the algorithmic process whereby a function can call itself) if its base-case is not met, in
# order to solve for the base-case. Once the base-case is found, all other numbers can be expanded back out and
# solved to n.
#
# ** NOTE: My solution works fine and I tested it up to n == 125! without any issues (16 GB RAM, 64-bit OS) but I
# did not attempt to implement more complicated solutions that might be able to handle larger numbers (or even
# decimal values) because the sieves involved were above my pay-grade. If that was the goal of the project, please
# let me know.
# ------------------------------------------------------------------------------------------------------------------
from termcolor import cprint
#  =============================================    SET UP    =======================================================


#  ============================================    PROCESSING    ====================================================
def factorial_number(n):							# passed-in value (n)
	if n < 0:
		raise ValueError(cprint("ValueError: cannot use this function for values less than zero.", 'red'))
	elif n == 0: 									# 0! == 1
		return 1									# return 1
	else:
		return n * factorial_number(n - 1)			# return recursive statement of n * function((n-1)!)

#  ==============================================    OUT-PUT    =====================================================


if __name__ == "__main__":
	msg = int(input("Enter in a whole, non-negative integer for the factorial function (1 - 100): "))
	val = factorial_number(msg)
	print()
	print(val)
