import logging
import logging.handlers
from datetime import datetime


time_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
no_time_format = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"
now = datetime.now()
time_formatter = logging.Formatter(time_format)
no_time_formatter = logging.Formatter(no_time_format)

#file Logger
file_handler = logging.FileHandler(now.strftime("%Y%m%d")+'.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(time_formatter)


#Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(time_formatter)

#SysLog
HOST, PORT = "127.0.0.1", 514
syslog_handler = logging.handlers.DatagramHandler(HOST, PORT)
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(no_time_formatter)

#Root Logger
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