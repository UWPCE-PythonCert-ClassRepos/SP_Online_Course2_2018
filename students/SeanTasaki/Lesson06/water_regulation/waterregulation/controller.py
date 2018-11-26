"""
Encapsulates command and coordination for the water-regulation module
"""

from waterregulation.decider import *

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
        main controller function
        """

        cur_height = self.sensor.measure()
        cur_pump_status = self.pump.get_state()
        height_status = self.decider.height_checker(cur_height)
        update = self.pump_status(cur_pump_status)
        # logging.info(f'{update}')
        update2 = update(height_status)
        try:
            if self.pump.set_state(update2):
                return True
            raise Exception('Pump did not ackowledge new action.')
        except Exception as e:
            print(e)

    def pump_status(self, cur_pump_status):
        """
        calls decider closer function to relay pump status
        """

        if cur_pump_status == 0:
            # logging.info(Decider.decide_pump_action(0, self.actions))
            return Decider.decide_pump_action(0, self.actions)
        if cur_pump_status == 1:
            # logging.info(Decider.decide_pump_action(0, self.actions))
            return Decider.decide_pump_action(1, self.actions)
        # logging.info(Decider.decide_pump_action(0, self.actions))
        return Decider.decide_pump_action(-1, self.actions)
