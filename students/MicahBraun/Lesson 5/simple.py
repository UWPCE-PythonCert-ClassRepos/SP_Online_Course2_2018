# ----------------------------------------------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: simple.py
# DATE CREATED: 10/11/2018
# UPDATED: 
# PURPOSE: Assignment 5: Logging
# DESCRIPTION: Modifications to the program simple.py to enable to the program to send log messages to a "remote
# server" (in this case, a dummy server syslogserver.py) regarding a running program's stability. The program
# needed to be able to handle logging levels differently in terms of formatting (per instructor's guidelines).
# ------------------------------------------------------------------------------------------------------------------
#  =============================================    SET UP    =======================================================
import logging
import logging.handlers
from datetime import date

print_out = "%(asctime)s %(filename)s: %(lineno)-3d %(levelname)s %(message)s"      # formatter 1 (w/ date)
print_out_no_date = "%(filename)s: %(lineno)-3d %(levelname)s %(message)s"          # formatter 2 (w/o date)

formatter = logging.Formatter(print_out)                                # set logging.Formatter to formatter 1
formatter_no_date = logging.Formatter(print_out_no_date)                # set logging.Formatter to formatter 2

file_handler = logging.FileHandler(date.today().isoformat() + '.log')   # all messages >= WARNING to-file
file_handler.setLevel(logging.WARNING)                                  # level set to WARNING
file_handler.setFormatter(formatter)                                    # formatter 1 is preset

console_handler = logging.StreamHandler()                               # log out put to console w/ StreamHandler
console_handler.setLevel(logging.DEBUG)                                 # all log levels >= DEBUG
console_handler.setFormatter(formatter)                                 # formatter 1 is preset

remote_handler = logging.handlers.DatagramHandler('127.0.0.1', 514)     # server handler (Windows: address, port)
remote_handler.setLevel(logging.ERROR)                                  # log levels >= ERROR
remote_handler.setFormatter(formatter_no_date)                          # formatter 2 is preset

logger = logging.getLogger()                                            # instantiate logger variable
logger.setLevel(logging.DEBUG)                                          # set level to DEBUG and higher
logger.addHandler(file_handler)                                         # add Handler for file_Handler
logger.addHandler(console_handler)                                      # add Handler for console_Handler
logger.addHandler(remote_handler)                                       # add Handler for remote_Handler

#  ============================================    PROCESSING    ====================================================
# simple.py


def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            i / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. Recovered gracefully.".format(i))


#  ==============================================    OUT-PUT    =====================================================


if __name__ == "__main__":
    my_fun(100)
