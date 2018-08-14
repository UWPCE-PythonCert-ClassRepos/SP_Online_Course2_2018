import logging
from datetime import datetime
from logging.handlers import DatagramHandler

format1 = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"  
format2 = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"  

formatter1 = logging.Formatter(format1)
formatter2 = logging.Formatter(format2)

file_handler = logging.FileHandler(datetime.today().strftime('%Y-%m-%d')+'.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter1)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter1)

stream_handler = DatagramHandler('127.0.0.1', 514)
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(formatter2)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(stream_handler)

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