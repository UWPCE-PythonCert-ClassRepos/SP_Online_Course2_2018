#Lesson 5 Logging Assignment

import logging
from logging.handlers import SysLogHandler
from time import strftime

#Output error message to Remote machine (with this address, this host machine)
#SyslogHandler makes connection to syslogserver.py
syslog_handler = SysLogHandler(address=('127.0.0.1', 514))
syslog_handler.setLevel(logging.ERROR)

#format the date and time for the output
#Output to file in this machine
#only cares about warning
#setLevel is let file handler know what to care.
format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
file_handler = logging.FileHandler(strftime("mylogfile_%H_%M_%m_%d_%Y.log"))
formatter = logging.Formatter(format)
file_handler.setLevel(logging.WARNING)         
file_handler.setFormatter(formatter)

#Output to the console (Terminal)
#StreamHandler is output to console
console_handler = logging.StreamHandler()        
console_handler.setLevel(logging.ERROR)          
console_handler.setFormatter(formatter)          

#add handlers. Without adding, it doesn't execute. 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)                   
logger.addHandler(file_handler)
logger.addHandler(console_handler)               
logger.addHandler(syslog_handler)

#custom script
def my_fun(n):
    for i in range(0,n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            i / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))


if __name__ == "__main__":
    my_fun(100)
