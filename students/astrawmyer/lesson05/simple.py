# simple.py
import logging

logging.basicConfig(level=logging.WARNING)
def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:                                   # Add this line
            logging.warning("The value of i is 50.")  # Add this line
        100 / (50 - i)

if __name__ == "__main__":
    my_fun(100)