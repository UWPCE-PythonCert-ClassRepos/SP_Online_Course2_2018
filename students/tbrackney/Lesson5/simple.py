"""
File Name: simple.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 2/20/2019
"""

import logging
from logging import handlers
from datetime import datetime

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
syslog_format = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

local_formatter = logging.Formatter(log_format)
syslog_formatter = logging.Formatter(syslog_format)

file_name = "{}.log".format(datetime.now().strftime("%Y-%m-%d"))
file_handler = logging.FileHandler(file_name)
file_handler.setLevel(logging.WARNING)           # Add this line
file_handler.setFormatter(local_formatter)

console_handler = logging.StreamHandler()        # Add this line
console_handler.setLevel(logging.DEBUG)          # Add this line
console_handler.setFormatter(local_formatter)          # Add this line

# Had to update syslogserver.py to use 127.0.0.1
syslog_handler = handlers.SysLogHandler(address=('127.0.0.1', 514))
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(syslog_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)                   # Add this line
logger.addHandler(file_handler)
logger.addHandler(console_handler)               # Add this line
logger.addHandler(syslog_handler)


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
