#Lesson 5 Logging Assignment:

import logging
from logging.handlers import SysLogHandler
import sys
from time import strftime

syslog_handler = SysLogHandler(address='127.0.0.1', 514)
syslog_handler.setLevel(logging.ERROR)
app.logger.addHandler(syslog_handler)


format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
file_Handler = logging.FileHandler(strftime("mylogfile_%H_%M_%m_%d_%Y.log"))


# Create a "formatter" using our format string
formatter = logging.Formatter(format)

# Create a log message handler that sends output to the file 'mylog.log'
#file_handler = logging.FileHandler('mylog.log') 
file_handler.setLevel(logging.WARNING)           # Add this line
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()        # Add this line
console_handler.setLevel(logging.DEBUG)          # Add this line
console_handler.setFormatter(formatter)          # Add this line

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)                   # Add this line
logger.addHandler(file_handler)
logger.addHandler(console_handler)               # Add this line

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
