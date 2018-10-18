#simple.py
# assignement 5 logging
__author__ = "Wieslaw Pucilowski"
import datetime
import logging
from logging import handlers


LogFile = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
syslog_format = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter = logging.Formatter(format)
formatter_syslog = logging.Formatter(syslog_format)

file_handler = logging.FileHandler(LogFile)
file_handler.setLevel(logging.WARNING)           
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()        
console_handler.setLevel(logging.DEBUG)          
console_handler.setFormatter(formatter)

syslog_handler = logging.handlers.SysLogHandler(address=('localhost', 514),
                                               # facility=LOG_USER,
                                               # socktype=socket.SOCK_DGRAM
                                               )
syslog_handler.setLevel(logging.ERROR)          
syslog_handler.setFormatter(formatter_syslog)

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
