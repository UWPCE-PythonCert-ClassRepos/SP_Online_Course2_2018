#!/usr/bin/python
import logging
import logging.handlers
from datetime import datetime

log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
log_format_2 = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"


formatter = logging.Formatter(log_format)
formatter_2 = logging.Formatter(log_format_2)


file_handler = logging.FileHandler('{:%Y-%m-%d}.log'.format(datetime.now()))
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

server_handler = logging.handlers.DatagramHandler('127.0.0.1', 514)
server_handler.setLevel(logging.ERROR)
server_handler.setFormatter(formatter_2)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(server_handler)


def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            100/(50-i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

if __name__ == '__main__':
    my_fun(100)

