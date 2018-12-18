#simple.py

import logging
from logging import handlers
from datetime import date

current_date = date.today().isoformat()

log_format1 = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
log_format2 = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"

formatter1 = logging.Formatter(log_format1)
formatter2 = logging.Formatter(log_format2)

file_handler = logging.FileHandler(f'{current_date}.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter1)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter1)

server_handler = logging.handlers.DatagramHandler('127.0.0.1', 514)
server_handler.setLevel(logging.ERROR)
server_handler.setFormatter(formatter2)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(server_handler)

#logging.basicConfig(level=logging.WARNING, format=log_format, filename='mylog.log')

def my_fun(n):
    for i in range(0, n):
        logging.debug(i)
        if i == 50:
            logging.warning("The value of i is 50.")
        try:
            100 / (50 - i)
        except ZeroDivisionError:
            logging.error(f'Tried to divide by zero. Variable i was {i}. Recovered gracefully.')
        
if __name__ == "__main__":
    my_fun(100)