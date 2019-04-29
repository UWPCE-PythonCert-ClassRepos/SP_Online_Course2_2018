import logging
from datetime import datetime
from logging import handlers

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
sys_format = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"

current_time = datetime.now()
formatted_date = current_time.strftime("%Y%m%d")

formatter = logging.Formatter(log_format)
server_formatter = logging.Formatter(sys_format)

file_handler = logging.FileHandler(f'{formatted_date}.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

sys_handler = logging.handlers.SysLogHandler(address=('0.0.0.0',514))
sys_handler.setLevel(logging.ERROR)
sys_handler.setFormatter(sys_format)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(sys_handler)

def my_fun(n):
	for i in range(0, n):
		logging.debug(i)
		if(i == 50):
			logging.warning("The value of i is 50.")
		try:
			100/(50 - i)
		except ZeroDivisionError:
			logging.error("Tried to divide by zero. Var i ws {}. Recovered gracefuly.".format(i))


if __name__ == "__main__":

	my_fun(100)
