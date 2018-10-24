#!/usr/bin/env python3

# simple.py

import logging

#logging.basicConfig(level=logging.WARNING) #prints log to console
#log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s" 
#logging.basicConfig(level=logging.WARNING, format=log_format)
#logging.basicConfig(level=logging.WARNING, format=log_format, filename='mylog.log')

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

# Create a "formatter" using our format string
formatter = logging.Formatter(log_format)

# Create a log message handler that sends output to the file 'mylog.log'
file_handler = logging.FileHandler('mylog.log') 
# Set the formatter for this log message handler to the formatter we created above.
file_handler.setFormatter(formatter)

# Get the "root" logger. More on that below.
logger = logging.getLogger()
# Add our file_handler to the "root" logger's handlers.
logger.addHandler(file_handler)

def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            100 / (50 - i)
        except ZeroDivisionError:
            logging.error(
                "Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

# def my_fun2(n):
#     logging.info("Function my_fun called with value {}".format(n))
#     my_fun(n)


if __name__ == "__main__":
    my_fun(100)
