#simple.py
import logging
import logging.handlers
import time as t


log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter = logging.Formatter(log_format)

run_time = t.asctime(t.localtime()).replace(' ', '_')
file_handler = logging.FileHandler('simple_'+run_time+'.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

server_format = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"
server_formatter = logging.Formatter(server_format)
server_handler = logging.handlers.SysLogHandler()
server_handler.setLevel(logging.ERROR)
server_handler.setFormatter(server_formatter)

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
