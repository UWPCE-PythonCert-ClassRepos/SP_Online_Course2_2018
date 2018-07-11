
import logging
import datetime
import logging.handlers

# get current date
current_date = datetime.datetime.now().strftime("%m-%d-%Y")

# format for log message
format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"

# format for the server log message
sys_format = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"

# create a "formatter" using format string
formatter = logging.Formatter(format)

# new formatter for the server loggng
sys_formatter = logging.Formatter(sys_format)

# create a log message handler that sends output to the file 'currentdate.log'
file_handler = logging.FileHandler(current_date+'.log')
file_handler.setLevel(logging.WARNING)
# set the formatter for this log message handler to the formatter we created above
file_handler.setFormatter(formatter)

# create a log message handler for the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# create a log message handler for the syslog server
sys_handler = logging.handlers.SysLogHandler(address=('127.0.0.1', 514))
#sys_handler = logging.handlers.DatagramHandler('127.0.0.1', 514)
sys_handler.setLevel(logging.ERROR)
sys_handler.setFormatter(sys_formatter)


# get the "root" logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# add our file_handler to the "root" logger's handlers
logger.addHandler(file_handler)

# add our console_handler to the "root" logger's handlers
logger.addHandler(console_handler)

# add sys_handler to the "root" logger's handlers
logger.addHandler(sys_handler)


def my_fun(n):
    for i in range(0,n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            i/(50-i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))


if __name__ == "__main__":
    my_fun(100)