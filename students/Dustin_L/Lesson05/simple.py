#!/usr/bin/env python3
import logging
import logging.handlers
from datetime import date

format_str = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
sys_format_str = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"

gen_formatter = logging.Formatter(format_str)

file_handler = logging.FileHandler(f'{date.today()}.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(gen_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(gen_formatter)

syslog_formatter = logging.Formatter(sys_format_str)
syslog_handler = logging.handlers.SysLogHandler(address=("127.0.0.1", 514))
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(syslog_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(syslog_handler)


def my_func(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
            try:
                i / (50 - i)
            except ZeroDivisionError:
                logging.error(f"Tried to divide by zero, Var i was {i}. "
                              f"Recovered gracefully")


if __name__ == '__main__':
    my_func(100)
