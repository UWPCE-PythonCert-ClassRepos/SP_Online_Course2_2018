import logging
import logging.handlers
import time

format_default = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
format_syslog = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter_default = logging.Formatter(format_default)
formatter_syslog = logging.Formatter(format_syslog)

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")
console_handler.setFormatter(formatter_default)

file_handler = logging.FileHandler('{}.log'.format(time.strftime("%Y-%m-%d")))
file_handler.setLevel("WARNING")
file_handler.setFormatter(formatter_default)

sys_handler = logging.handlers.SysLogHandler(address=("0.0.0.0", 514))
sys_handler.setLevel("ERROR")
sys_handler.setFormatter(formatter_syslog)

logger = logging.getLogger()
logger.setLevel("DEBUG")
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(sys_handler)


def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            i / (50 - i)
        except ZeroDivisionError:
            logging.error("Tried to divide by zero. Var i was {}. "
                          "Recovered gracefully.".format(i))


if __name__ == "__main__":
    my_fun(100)
