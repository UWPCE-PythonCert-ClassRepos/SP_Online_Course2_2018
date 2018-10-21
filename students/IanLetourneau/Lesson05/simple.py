#!/usr/bin/env python3
# Ian Letourneau
# 10/5/2018

import logging
from logging import handlers
from datetime import datetime

format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter1 = logging.Formatter(format)

format = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter2 = logging.Formatter(format)

sys_handler = logging.handlers.DatagramHandler("127.0.0.1", 514)
sys_handler.setLevel(logging.ERROR)
sys_handler.setFormatter(formatter2)

now = datetime.now()

file_name = "{}_{}_{}.log".format(str(now.day), str(now.month), str(now.year))
file_handler = logging.FileHandler(file_name)
file_handler.setLevel(logging.WARNING)           # Add this line
file_handler.setFormatter(formatter1)

console_handler = logging.StreamHandler()        # Add this line
console_handler.setLevel(logging.NOTSET)          # Add this line
console_handler.setFormatter(formatter1)          # Add this line

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)                   # Add this line
logger.addHandler(file_handler)
logger.addHandler(console_handler) 
logger.addHandler(sys_handler)             

def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            i / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

if __name__ == "__main__":
    my_fun(100)