# simple.py

import logging
from datetime import date
# need this for sysloghandler
import logging.handlers

format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
# Without time
format2 = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"

formatter = logging.Formatter(format)
# second formatter without time
formatter2 = logging.Formatter(format2)

# File name with date, format has date
file_handler = logging.FileHandler('{}.log'.format(date.today()))
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

# New SysLogHandler, with level Error, and format without time
syslog_handler = logging.handlers.SysLogHandler()
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(formatter2)

# By default the stream will be printed to the console
console_handler = logging.StreamHandler()       
console_handler.setLevel(logging.DEBUG)          
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) 
logger.addHandler(file_handler)
logger.addHandler(console_handler) 
# third handler to send messages to syslog server
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