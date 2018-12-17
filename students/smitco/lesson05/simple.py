# lesson 05 logging exercise
# !/usr/bin/env python3

import logging
import logging.handlers
import datetime

format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter = logging.Formatter(format)

format_no_time = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter_no_time = logging.Formatter(format_no_time)

current = datetime.datetime.now()
date = [str(current.month), str(current.day), str(current.year)]
current_date = "_".join(date)
file_name = "{}.log".format(current_date)
file_handler = logging.FileHandler(file_name)
file_handler.setLevel(logging.WARNING)           
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()        
console_handler.setLevel(logging.DEBUG)          
console_handler.setFormatter(formatter)  

server_host = "127.0.0.1"
server_port = 514
server_handler = logging.handlers.DatagramHandler(server_host, server_port)
server_handler.setLevel(logging.ERROR)
server_handler.setFormatter(formatter_no_time)        

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