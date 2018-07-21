import logging
import logging.handlers
from datetime import date

format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
system_format = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter = logging.Formatter(format)
system_formatter = logging.Formatter(system_format)

file_handler = logging.FileHandler(date.today().isoformat() + '.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)



remote_handler = logging.handlers.DatagramHandler('127.0.0.1', 514)
remote_handler.setLevel(logging.ERROR)
remote_handler.setFormatter(system_formatter)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(remote_handler)

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