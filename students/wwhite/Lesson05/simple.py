#!/usr/bin/env python

# simple.py
import logging
import logging.handlers
import datetime

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
sys_log_format = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"

formatter = logging.Formatter(log_format)
sys_log_formatter = logging.Formatter(sys_log_format)

file_handler = logging.FileHandler(f'{datetime.date.today()}.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

sys_log_handler = logging.handlers.SysLogHandler(address=("127.0.0.1", 514))
sys_log_handler.setLevel(logging.ERROR)
sys_log_handler.setFormatter(sys_log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(sys_log_handler)


def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            100 / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))


if __name__ == "__main__":
    my_fun(100)

