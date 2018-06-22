# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 09:19:41 2018

@author: Karl M. Snyder
"""
import logging

format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

#logging.basicConfig(format=format, level=logging.WARNING, filename='mylog.log')

formatter = logging.Formatter(format)

file_handler = logging.FileHandler('mylog.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler= logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.") #after we debugged to find 50 causes crash
        try:
            i / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

#logging.critical("This is a critical error!")
#logging.error("I'm an error.")
#logging.warning("Hello, I'm a warning!")
#logging.info("This is some information")
#logging.debug("Perhaps this information will help you find your problems?")


if __name__ == "__main__":
    my_fun(100)