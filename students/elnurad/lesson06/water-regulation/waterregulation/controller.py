"""
Encapsulates command and coordination for the water-regulation module
"""


#  pylint: disable = too-few-public-methods
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
            'PUMP_IN': pump.PUMP_IN,
            'PUMP_OUT': pump.PUMP_OUT,
            'PUMP_OFF': pump.PUMP_OFF,
        }

    def tick(self):
        """
        Tick method for controller class.
        """
        current_height = self.sensor.measure()
        current_action = self.pump.get_state()
        state = self.decider.decide(current_height, current_action,
                                    self.actions)
        return self.pump.set_state(state)
