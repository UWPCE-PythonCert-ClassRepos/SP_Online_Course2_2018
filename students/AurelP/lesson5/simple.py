#!/usr/bin/python
#Lesson 5 Aurel Perianu

# simple.py
import logging
import logging.handlers
#import datetime
from datetime import date

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
log_syslog = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

#formatter = logging.Formatter(log_format)
formatter_syslog = logging.Formatter(log_syslog)

syslog_handler = logging.handlers.SysLogHandler(address=('0.0.0.0',514))
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(formatter_syslog)

formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler(str(date.today())+'.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(syslog_handler)


def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:                                   # Add this line
            logging.warning("The value of i is 50.")  # Add this line
        try:
            100 / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))
        #100 / (50 - i)

if __name__ == "__main__":
    my_fun(100)
