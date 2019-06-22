import datetime
import logging

from logging.handlers import SysLogHandler
from logging.handlers import DatagramHandler

log_format_server = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter_server = logging.Formatter(log_format_server)
formatter = logging.Formatter(log_format)


file_handler = logging.FileHandler('mylog.log')
file_handler.setLevel(logging.WARNING)           # Add this line
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()        # Add this line
console_handler.setLevel(logging.DEBUG)          # Add this line
console_handler.setFormatter(formatter)          # Add this line

syslog_handler = DatagramHandler('0.0.0.0', 514)
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(formatter_server)

logger = logging.getLogger()

logger.addHandler(syslog_handler)
logger.setLevel(logging.DEBUG)                   # Add this line
logger.addHandler(file_handler)
logger.addHandler(console_handler)               # Add this line

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
