''' 
    Test the time difference to execute using normal python vs. pypy
    Creates a matrix of 10 values per row and performs simple moving average
    Rounds the moving averages and saves to a list
'''


import time

start = time.time()

import logging
import random
from datetime import date

format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

formatter_no_datetime = logging.Formatter(format)

file_handler = logging.FileHandler(str(date.today())+'.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter_no_datetime)

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
logger.addHandler(file_handler)

dat = [[random.randint(0, 10) for x in range(10)] for x in range(500000)]
for d in dat:
    logging.debug(d)

N = 3
out_moving_aves = []
for d in dat:
    cumsum, moving_aves = [0], []

    for i, x in enumerate(d, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

    moving_aves = [None] * (N - 1) + [round(elem, 2) for elem in moving_aves]
    logging.debug(moving_aves)
    out_moving_aves.append(moving_aves)


end = time.time()
logging.warning('The process took approx: {: .0f} seconds'.format(end - start))
# Python base takes 12 seconds and pypy takes less than half the time at 5 seconds