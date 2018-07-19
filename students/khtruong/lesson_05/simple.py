#!/usr/bin/env python
import logging
import datetime
from logging.handlers import SysLogHandler


format1 = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
format2 = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter1 = logging.Formatter(format1)
formatter2 = logging.Formatter(format2)

file_handler = logging.FileHandler('{}.log'.format(datetime.date.today()))
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter1)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter1)

syslog_handler = SysLogHandler(address=('127.0.0.1', 514))
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(formatter2)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(syslog_handler)


def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            i / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. "
                          "Recovered gracefully.".format(i))

if __name__ == "__main__":
    my_fun(100)
