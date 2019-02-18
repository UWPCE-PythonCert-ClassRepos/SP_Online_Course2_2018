"""
Encapsulates command and coordination for the water-regulation module
"""


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

        self.actions = {
            'PUMP_IN': pump.PUMP_IN,
            'PUMP_OUT': pump.PUMP_OUT,
            'PUMP_OFF': pump.PUMP_OFF,
        }

    def tick(self):
        """
        On each call to tick, the controller shall:

          1. query the sensor for the current height of liquid in the tank
          2. query the pump for its current state (pumping in,
            pumping out, or at rest)
          3. query the decider for the next appropriate state of the pump,
            given the above
          4. set the pump to that new state

        :return: True if the pump has acknowledged its new state, else False
        """
        measurement = self.get_measurement()
        pump_state = self.get_pump_state()
        new_pump_state = self.decide_pump_state(current_height=measurement,
                                                pump_state=pump_state,
                                                actions=self.actions)
        return new_pump_state()

    def get_measurement(self) -> float:
        """calls sensor method for getting measurement
        reading of liquid level.  No inputs.

        :return: float with response from sensor
        """
        return float(self.sensor.measure())

    def get_pump_state(self) -> str:
        """calls pump to get current pump state.sensor

        :return: int indicating state of pump
        """
        return self.pump.get_state()

    def decide_pump_state(self, current_height: float,
                          pump_state: str,
                          actions: dict) -> str:
        """analyzes current state of system and decides command for pump
        :returns: str indicating command to send to pump"""
        return self.decider.decide(current_height=current_height,
                                   current_action=pump_state,
                                   actions=actions)
