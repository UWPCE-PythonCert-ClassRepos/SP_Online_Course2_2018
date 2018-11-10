'''
Sean Tasaki
11/6/2018
Lesson05
'''

import logging
import logging.handlers 
import datetime

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s" 
syslog_format = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"

formatter = logging.Formatter(log_format)
syslog_formatter = logging.Formatter(syslog_format)

file_handler = logging.FileHandler('{}.log'.format(datetime.datetime.today().strftime('%Y-%m-%d')))
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()     
console_handler.setLevel(logging.DEBUG)       
console_handler.setFormatter(formatter)

remote_handler = logging.handlers.SysLogHandler(address=('127.0.0.1', 514))
remote_handler.setLevel(logging.ERROR)
remote_handler.setFormatter(syslog_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(remote_handler)

#logging.basicConfig(level=logging.INFO, format=log_format, filename='mylog.log')                  

def my_fun(n):
    logging.info("Function my_fun called with value {}".format(n))
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            100 / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))

if __name__ == "__main__":
    my_fun(100)