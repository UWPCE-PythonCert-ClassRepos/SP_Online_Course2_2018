"""
Encapsulates command and coordination for the water-regulation module
"""


class Controller():
    """
    Encapsulates command and coordination for the water-regulation module
    """

    def __init__(self, sensor, pump, decider):
        """
        Create a new controller

        :param sensor: Typically an instance of sensor.Sensor
        :param pump: Typically an instance of pump.Pump
        :param decider: Typically an instance of decider.Decider
        """

        self.sensor = sensor
        self.pump = pump
        self.decider = decider

        self.actions = {
            'PUMP_IN': 'PUMP_IN',
            'PUMP_OUT': 'PUMP_OUT',
            'PUMP_OFF': 'PUMP_OFF',
        }

    def tick(self):
        """
        On each call to tick, the controller shall:

          1. query the sensor for the current height of liquid in the tank
          2. query the pump for its current state (pumping in, out, or off)
          3. query the decider for the next appropriate state of the pump
          4. set the pump to that new state

        :return: True if the pump has acknowledged its new state, else False
        """

        height = self.sensor.measure()
        action = self.pump.get_state()
        decision = self.decider.decide(height, action)

        self.pump.set_state(decision)
