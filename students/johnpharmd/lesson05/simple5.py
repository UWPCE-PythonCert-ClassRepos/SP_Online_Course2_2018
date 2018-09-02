#!/usr/bin/env python3

# simple.py
import logging
import logging.handlers
from datetime import date
format1 = '%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s'
format2 = '%(filename)s:%(lineno)-4d %(levelname)s %(message)s'

# logging.basicConfig(level=logging.WARNING, format=format1,
#                     filename='mylog.log')
# BEGIN NEW ITEMS [basicConfig commented out at this point]
formatter1 = logging.Formatter(format1)
formatter2 = logging.Formatter(format2)

file_handler = logging.FileHandler('{}.log'.format(date.today()))
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter1)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter1)

syslog_handler = logging.handlers.SysLogHandler(address=('127.0.0.1', 514))
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(formatter2)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger_dict = {1: console_handler, 2: file_handler, 3: syslog_handler}
for num, handler in logger_dict.items():
    logger.addHandler(handler)


# logger1 = logging.getLogger()
# logger1.setLevel(logging.DEBUG)
# logger1.addHandler(console_handler)
# logger2 = logging.getLogger()
# logger2.setLevel(logging.WARNING)
# logger2.addHandler(file_handler)
# logger3 = logging.getLogger()
# logger3.setLevel(logging.ERROR)
# logger3.addHandler(syslog_handler)
# END NEW ITEMS


def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning('The value of i is 50.')
        try:
            i / (50 - i)
        except ZeroDivisionError:
            logging.error('Tried to divide by zero. Var i was {}. '
                          'Recovered gracefully.'.format(i))


if __name__ == '__main__':
    my_fun(100)
