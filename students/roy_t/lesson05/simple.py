#!/usr/bin/env python3


import logging, logging.handlers
from datetime import datetime


def configure_logging():
    current_date = datetime.now().date().strftime('%Y-%m-%d')
    # FORMATTERS
    format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter = logging.Formatter(format)
    format_no_date = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    formatter_error = logging.Formatter(format_no_date)

    # FILE HANDLERS
    file_handler = logging.FileHandler(f'{current_date}.log')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    file_handler_error = logging.FileHandler('error.log')
    file_handler_error.setLevel(logging.ERROR)
    file_handler_error.setFormatter(formatter_error)

    # CONSOLE HANDLER
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # NETWORK HANDLER
    syslog_handler = logging.handlers.SysLogHandler(address=('127.0.0.1', 514))
    # dg_handler = logging.handlers.DatagramHandler(host='127.0.0.1', port=514)

    # LOGGER
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(file_handler_error)
    logger.addHandler(console_handler)
    logger.addHandler(syslog_handler)
    # logger.addHandler(dg_handler)

    # # ADD SOME LOG MESSAGES
    # logging.warning('WARNING_TEST1: Date and time should be logged')
    # logging.error('ERROR_TEST1: Date and time should NOT be logged')
    # logging.warning('WARNING_TEST2: Date and time should be logged.')
    # logging.info('INFO_TEST1: General test message here.')
    # logging.error('ERROR_TEST2: Date and time should not be logged.')

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
    configure_logging()
    my_fun(100)
