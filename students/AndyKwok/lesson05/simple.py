# Name: Andy Kwok
# Note: Updated with notes to self

from time import strftime
import logging
from logging.handlers import SysLogHandler

# Setup preferred format for the logging function
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)

log_format_alt = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter_alt = logging.Formatter(log_format_alt)

# Setup type of desired output, type of message to record, and expected format
file_handler = logging.FileHandler(strftime("%Y_%m_%d.log"))
file_handler.setLevel(logging.WARNING)           
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()        
console_handler.setLevel(logging.DEBUG)          
console_handler.setFormatter(formatter)  

server_handler = SysLogHandler(address=('127.0.0.1', 514))
server_handler.setLevel(logging.ERROR)
server_handler.setFormatter(formatter_alt)    

# Actual logging processor, message filter level, types of logging output (file, console, server) 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)                   
logger.addHandler(file_handler)
logger.addHandler(console_handler)               
logger.addHandler(server_handler)

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