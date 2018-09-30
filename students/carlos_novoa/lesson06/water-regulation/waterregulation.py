"""
For running and testing of water regulation projet
"""

from pump import Pump
# from sensor import Sensor
# from .controller import Controller
# from .decider import Decider


def reg():
    # sensor = Sensor('127.0.0.1', 8000)
    pump = Pump('127.0.0.1', 8080)
    # decider = Decider(50, .05)
    # controller = Controller(sensor, pump, decider)
    # controller.tick()
    print('inside reg() method')
    pump_state = pump.get_state()
    # return pump_state


if __name__ == "__main__":
    reg()
