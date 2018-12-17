'''
Sean Tasaki
11/25/2018
Lesson06
'''

import decider
import sensor
import controller
import pump


if __name__ == '__main__':

    DECIDER = decider.Decider(5, 1)
    SENSOR = sensor.Sensor('127.0.0.1', 8000)
    PUMP = pump.Pump('100.9.9.0', 9000)
    CONTROLLER = controller.Controller(SENSOR, PUMP, DECIDER)
