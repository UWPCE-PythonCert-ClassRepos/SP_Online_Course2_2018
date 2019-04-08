"""
Encapsulates command and coordination for the water-regulation module
"""
import logging
logging.basicConfig(level=logging.ERROR)


class Controller:
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
        self.liquid_level = int()
        self.pump_status = int()
        self.control_decision = int()

        self.actions = {
            'PUMP_IN': pump.PUMP_IN,
            'PUMP_OUT': pump.PUMP_OUT,
            'PUMP_OFF': pump.PUMP_OFF,
        }

    def tick(self):
        """
        On each call to tick, the controller shall:

          1. query the sensor for the current height of liquid in the tank
          2. query the pump for its current state (pumping in, pumping out,
            or at rest)
          3. query the decider for the next appropriate state of the pump,
            given the above
          4. set the pump to that new state

        :return: True if the pump has acknowledged its new state, else False
        """

        # query the sensor for the current height of liquid in the tank
        self.liquid_level = self.sensor.measure()
        logging.debug('In Controller, the value of liquid_level is %s',
                      self.liquid_level)

        # query the pump for its current state
        # (pumping in, pumping out, or at rest)
        self.pump_status = self.pump.get_state()
        logging.debug('In Controller, '
                      'the value of current state of pump is %s',
                      self.pump_status)

        # query the decider for the next appropriate state
        # of the pump, given the above
        self.control_decision = self.decider.decide(self.liquid_level,
                                                    self.pump_status,
                                                    self.actions)
        logging.debug('In Controller, the value of decision is %s',
                      self.control_decision)

        # set the pump
        self.pump.set_state(self.control_decision)

        # set the pump to that new state
        if not self.pump.set_state(self.control_decision):
            # Return False if pump has not acknowledged new state
            return False
        return True
