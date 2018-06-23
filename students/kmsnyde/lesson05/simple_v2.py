# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 09:19:41 2018

@author: Karl M. Snyder
"""
import datetime
import logging
import logging.handlers

format_a = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
format_b = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

#logging.basicConfig(format=format, level=logging.WARNING, filename='mylog.log')

formatter = logging.Formatter(format_a)
formatter1 = logging.Formatter(format_b)

file_handler = logging.FileHandler('{}.log'.format(datetime.date.today()))
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler= logging.StreamHandler()
console_handler.setLevel(logging.NOTSET)
console_handler.setFormatter(formatter)

data_handler = logging.handlers.DatagramHandler('127.0.0.1', 514)
data_handler.setLevel(logging.ERROR)
data_handler.setFormatter(formatter1)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(data_handler)



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