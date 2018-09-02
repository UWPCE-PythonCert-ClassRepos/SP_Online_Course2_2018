import logging
from logging.handlers import SysLogHandler, DatagramHandler
from datetime import datetime
from time import strftime

# Var setup
today_date = strftime("%Y-%m-%d")
default_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
sys_format = "%(filename)s:%(lineno)-3d %(levelname)s %(messages)s"

def_formatter = logging.Formatter(default_format)
sys_formatter = logging.Formatter(sys_format)

# Console - all log messages with streamhandler
console_handler = logging.StreamHandler()        
console_handler.setLevel(logging.DEBUG)          
console_handler.setFormatter(def_formatter)   

# Filehandler - warning and higher messages only, include current time
# filename: {todays-date}.log
# shares format with console/streamhandler
file_handler = logging.FileHandler(f'{today_date}.log')
file_handler.setLevel(logging.WARNING)           
file_handler.setFormatter(def_formatter)
       
# SysLog Server - error and higher messages only, does not include current time
sys_handler = DatagramHandler(host='127.0.0.1', port=514)
sys_handler.setLevel(logging.ERROR)
sys_handler.setFormatter(sys_formatter)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)                   
logger.addHandler(file_handler)
logger.addHandler(console_handler)    
logger.addHandler(sys_handler)           


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