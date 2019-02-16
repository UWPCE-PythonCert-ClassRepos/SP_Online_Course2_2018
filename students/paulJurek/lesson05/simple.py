#simple.py
import logging
from logging import handlers
import datetime

format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
format_no_time = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter = logging.Formatter(format)
sysserv_formatter = logging.Formatter(format_no_time)

file_handler = logging.FileHandler(datetime.datetime.now().strftime('%Y%m%d') + '.log')
file_handler.setLevel(logging.WARNING)           
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()        
console_handler.setLevel(logging.DEBUG)          
console_handler.setFormatter(formatter)

sysserv_handler = logging.handlers.DatagramHandler('127.0.0.1', 514)
sysserv_handler.setLevel(logging.ERROR)
sysserv_handler.setFormatter(sysserv_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)                   
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(sysserv_handler)               

def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            i / (50 - i)
        except ZeroDivisionError:
            # prefer exception over error as it brings traceback
            logging.exception("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

if __name__ == "__main__":
    my_fun(100)