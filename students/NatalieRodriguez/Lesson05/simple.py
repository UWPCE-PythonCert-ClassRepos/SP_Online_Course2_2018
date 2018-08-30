#Lesson 05 Logging Exercise
#Natalie Rodriguez
#August 22, 2018

#Assignment Requirements:
#1. log ALL messages to the console. The format should include the current time.
#2. WARNING and high messages should be logged to a filename {todays-date}.log.
# The format of these messages should include the current time.
#3. ERROR and higher messages should be logged to a syslog server.
# The syslog server will be appending its own time stamps to the messages that it receives,
# so DO NOT include the current time in the format (format2) of the log messages that you send to the server.


from datetime import datetime
import logging
import logging.handlers

format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
#My formatter below
format2 = "%(filename)s:%(lineno)-4d %(levelname)s %(message)s"

#Begin new stuff
#create a "formatter" using our format string
formatter = logging.Formatter(format)

#My formatter below
formatter2 = logging.Formatter(format2)

#create a log message handler that sends output to the file 'mylog.log'
file_handler = logging.FileHandler(datetime.now().strftime('%h_%d_%Y_%H%M_CST.log'))
file_handler.setLevel(logging.WARNING)
#Set the formatter for this log message handler to the formatter we created above.
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

#My additions below
sys_handler = logging.handlers.SysLogHandler(address=('127.0.0.1', 514))
sys_handler.setFormatter(formatter2)

#Get the "root" logger. More on that below.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#Add our file_handler to the "root" logger's handlers.
logger.addHandler(file_handler)
logger.addHandler(console_handler)
#End new stuff

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

