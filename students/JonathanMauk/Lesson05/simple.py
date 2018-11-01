# simple.py
#
# To complete this assignment, modify simple.py to satisfy the following goals:
#
# 1. You want ALL log messages logged to the console. The format of these messages should include the current time.
# 2. You want WARNING and higher messages logged to a file named { current-date }.log.
#    The format of these messages should include the current time.
# 3. You want ERROR and higher messages logged to a syslog server. The syslog server will be appending its own time
#    stamps to the messages that it receives, so DO NOT include the current time in the format of the log messages
#    that you send to the server.
#
# To complete this assignment, you will need to create:
#
# 1. A second instance of Formatter. Because the three different destinations for your log messages require two
#    different formats (one with time stamps and one without), you'll need two different instances of Formatter.
# 2. A third Handler, to send messages to the syslog server.

import logging
import datetime

format1 = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
format2 = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter1 = logging.Formatter(format1)
formatter2 = logging.Formatter(format2)

file_handler = logging.FileHandler(f'{datetime.date.today()}.log')
file_handler.setLevel(logging.WARNING)           
file_handler.setFormatter(formatter1)

console_handler = logging.StreamHandler()        
console_handler.setLevel(logging.DEBUG)          
console_handler.setFormatter(formatter)          

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)                   
logger.addHandler(file_handler)
logger.addHandler(console_handler)               


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
