#simple.py
import logging

import logging.handlers

from logging.handlers import SysLogHandler

from datetime import date


# Format and formatter for local logging
format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(format)

# Format and formatter for syslog server logging
format_syslog = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter_syslog = logging.Formatter(format_syslog)

# Log Warning level messages to log file
logfile = str(date.today()) + ".log"
file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.WARNING)           
file_handler.setFormatter(formatter)

# Log Debug level messages to console
console_handler = logging.StreamHandler()        
console_handler.setLevel(logging.DEBUG)          
console_handler.setFormatter(formatter)          

# Log Error level messages to server log
server_handler = SysLogHandler(address=('127.0.0.1', 514))        
server_handler.setLevel(logging.ERROR)          
server_handler.setFormatter(formatter_syslog)          


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