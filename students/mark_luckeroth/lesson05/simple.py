#!/usr/bin/env python3

#simple.py
import logging
import logging.handlers
import datetime as dt

cli_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
srvr_format = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

cli_formatter = logging.Formatter(cli_format)
srvr_formatter = logging.Formatter(srvr_format)

file_handler = logging.FileHandler(dt.date.today().strftime('%Y_%m_%d')+'.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(cli_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(cli_formatter)

HOST, PORT = "0.0.0.0", 514
server_handler = logging.handlers.SysLogHandler(address=('localhost', 514))
server_handler.setLevel(logging.ERROR)
server_handler.setFormatter(srvr_formatter)

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
            i / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

if __name__ == "__main__":
    my_fun(100)