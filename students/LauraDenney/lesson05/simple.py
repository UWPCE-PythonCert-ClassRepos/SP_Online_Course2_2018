#Laura Denney 4/16/19


# simple.py
import logging
import logging.handlers as hands

import datetime

now = datetime.datetime.now()

log_format = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"
time_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"  # Add/modify these
#logging.basicConfig(level=logging.WARNING, format=log_format,filename='mylog.log')

time_formatter = logging.Formatter(time_format)
formatter = logging.Formatter(log_format)

file_handler = logging.FileHandler('{}_{}_{}.log'.format(now.month,now.day,now.year))
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(time_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.NOTSET)
console_handler.setFormatter(time_formatter)

syslog_handler = hands.SysLogHandler(address=('127.0.0.1',514))
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(syslog_handler)

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