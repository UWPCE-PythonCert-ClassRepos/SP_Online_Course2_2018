

import logging
import datetime

# get current date
current_date = datetime.datetime.now().strftime("%m-%d-%Y")

# format for log message
format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"

# BEGIN NEW STUFF
# create a "formatter" using format string
formatter = logging.Formatter(format)

# create a log message handler that sends output to the file 'currentdate.log'
file_handler = logging.FileHandler(current_date+'.log')
file_handler.setLevel(logging.WARNING)
# set the formatter for this log message handler to the formatter we created above
file_handler.setFormatter(formatter)

# create a log message handler for the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# create a log message handler for the

# get the "root" logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# add our file_handler to the "root" logger's handlers
logger.addHandler(file_handler)

# add our console_handler to the "root" logger's handlers
logger.addHandler(console_handler)
# END NEW STUFF


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