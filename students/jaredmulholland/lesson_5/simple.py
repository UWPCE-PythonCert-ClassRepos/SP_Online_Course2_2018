#simple.py
import logging
from logging.handlers import SysLogHandler
import datetime

now = str(datetime.datetime.today().strftime('%Y_%m_%d'))
log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
log_format_file = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"


#begin new stuff
formatter = logging.Formatter(log_format)
formatter_file = logging.Formatter(log_format_file)

#file
file_handler = logging.FileHandler(now+'.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter_file)

#console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

#server
server_handler = SysLogHandler(address=('127.0.0.1',514))
server_handler.setLevel(logging.ERROR)
server_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(server_handler)

#end new stuff

def my_fun(n):
    for i in range(0,n):
        logging.debug(i)
        if i == 50:
            logging.warning("the value of i is 50.")
        try:
            100/(50-i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}".format(i))

if __name__ == "__main__":
    my_fun(100)