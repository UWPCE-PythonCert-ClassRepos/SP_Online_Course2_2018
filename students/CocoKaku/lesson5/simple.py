import logging
import logging.handlers
import datetime

# formatter for file and console handlers
log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"  # Add/modify these
formatter = logging.Formatter(log_format)

# file handler logs WARNING and higher to {todays-date}.log file
today = datetime.datetime.now().strftime("%Y-%m-%d")
file_handler = logging.FileHandler(f'{today}.log')
file_handler.setLevel(logging.WARNING)           # Add this line
file_handler.setFormatter(formatter)

# console handler logs DEBUG and higher to console
console_handler = logging.StreamHandler()        # Add this line
console_handler.setLevel(logging.DEBUG)          # Add this line
console_handler.setFormatter(formatter)          # Add this line

# formatter for syslog handler
syslog_format = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"
syslog_formatter = logging.Formatter(syslog_format)

# syslog handler logs ERROR and higher to syslog server
syslog_handler = logging.handlers.SysLogHandler(address=('0.0.0.0', 1024))
syslog_handler.setLevel(logging.ERROR)
syslog_handler.setFormatter(syslog_formatter)

# create logger and add handlers
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(syslog_handler)


def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            100 / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was %d. Recovered gracefully.", i)


if __name__ == "__main__":
    my_fun(100)
