import logging
import logging.handlers
import time

format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
log_timestr = time.strftime('%Y%m%d-%H%M%S')
filename = '{}.log'.format(log_timestr)

formatter = logging.Formatter(format)

file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

server_handler = logging.handlers.SysLogHandler(address=('127.0.0.1', 514))
server_handler.setLevel(logging.ERROR)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(server_handler)


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
