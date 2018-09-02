#simple.py
import logging, logging.handlers
import datetime
import syslogserver as ss

ss_format = "%(filename)s:%(lineno)-3d %(levelname)s %(message)s"
format = f"%(asctime)s {ss_format}"

ss_formatter = logging.Formatter(ss_format)
formatter = logging.Formatter(format)

file_handler = logging.FileHandler(datetime.date.today().isoformat() + '.log')
file_handler.setLevel(logging.WARNING)           
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()        
console_handler.setLevel(logging.DEBUG)          
console_handler.setFormatter(formatter)

system_handler = logging.handlers.SysLogHandler(('127.0.0.1', 514))
system_handler.setLevel(logging.ERROR)
system_handler.setFormatter(ss_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)                   
logger.addHandler(file_handler)
logger.addHandler(console_handler)               
logger.addHandler(system_handler)

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