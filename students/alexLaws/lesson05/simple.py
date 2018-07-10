#!/usr/bin/env python3

import logging
from logging.handlers import DatagramHandler
import datetime

format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
sysformat = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"

today = datetime.date.today()

formatter = logging.Formatter(format)
sysformatter = logging.Formatter(sysformat)

file_handler = logging.FileHandler('{}.log'.format(today))
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

syslog_handler = DatagramHandler("127.0.0.1", 514)
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(sysformatter)

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
