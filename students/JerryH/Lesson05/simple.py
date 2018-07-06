#simple.py
import logging
import datetime
from logging.handlers import SysLogHandler

now = datetime.datetime.now()
current_date = str(now.year) + str(now.month) + str(now.day)

format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
syslog_format = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter = logging.Formatter(format)
syslog_formatter = logging.Formatter(format)

file_handler = logging.FileHandler(current_date + '.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

syslog_handler = SysLogHandler(address=('127.0.0.1', 514))
# syslog_handler = DatagramHandler('127.0.0.1', 514)
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(syslog_formatter)

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
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))
if __name__ == "__main__":
    my_fun(100)
