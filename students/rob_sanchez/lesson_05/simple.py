#!/usr/bin/env python3
import logging
import logging.handlers
import datetime
import syslogserver

format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
syslog_format = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

# Create a "formatter" using our format string
formatter = logging.Formatter(format)
syslog_format = logging.Formatter(syslog_format)

# Create a log message handler that sends output to the file 'mylog.log'
file_handler = logging.FileHandler(str(datetime.date.today()) + '.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Syslog handler
syslog_handler = logging.handlers.SysLogHandler(address=(syslogserver.HOST, syslogserver.PORT))
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(syslog_format)

# Get the "root" logger.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(syslog_handler)


def my_fun(n):
    for i in range(0, n):

        logging.debug("Current variable: " + str(i))

        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            i / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))


if __name__ == "__main__":
    my_fun(100)
