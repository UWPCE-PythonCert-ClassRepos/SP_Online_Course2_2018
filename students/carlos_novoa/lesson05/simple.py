#!/usr/bin/env python3

# simple.py
import logging
import logging.handlers
import datetime

now = datetime.datetime.now()
date = now.strftime('%Y-%m-%d')

# default
format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(format)

# console
handler_cons = logging.StreamHandler()
handler_cons.setLevel(logging.NOTSET)
handler_cons.setFormatter(formatter)

# file
handler_file = logging.FileHandler(f"{date}.log")
handler_file.setLevel(logging.WARNING)
handler_file.setFormatter(formatter)

# server
format_serv = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter_serv = logging.Formatter(format_serv)
handler_serv = logging.handlers.SysLogHandler(address=("127.0.0.1", 514))

# logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler_cons)
logger.addHandler(handler_file)
logger.addHandler(handler_serv)


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
