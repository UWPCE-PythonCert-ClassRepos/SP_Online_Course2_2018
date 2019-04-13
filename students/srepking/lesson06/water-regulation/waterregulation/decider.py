"""
Encapsulates decision making in the water-regulation module
"""
import logging
logging.basicConfig(level=logging.DEBUG)


class Decider:
    """
    Encapsulates decision making in the water-regulation module
    """

    def __init__(self, target_height, margin):
        """
        Create a new decider instance for this tank.

        :param target_height: the target height for liquid in this tank
        :param margin: the margin of liquid above and below the target height
        for which the pump should not turn on. Ex: .05 represents a
        5% margin above and below the target_height.
        """

        self.target_height = target_height
        self.margin = margin
# If the pump is off and the height is below the margin region,
# then the pump should be turned to PUMP_IN.
        if self.target_height < 0:
            raise Exception('Bad Height Setting.')

    def decide(self, current_height, current_action, actions):
        """
        Decide a new action for the pump, given the current height of liquid
        in the tank and the current action of the pump.

        Note that the new action for the pump MAY be the same as the current
        action of the pump.

        The *decide* method shall obey the following behaviors:

          1. If the pump is off and the height is below the margin region,
          then the
             pump should be turned to PUMP_IN.
          2. If the pump is off and the height is above the margin region,
          then the
             pump should be turned to PUMP_OUT.
          3. If the pump is off and the height is within the margin region
          or on
             the exact boundary of the margin region, then the pump shall
             remain at
             PUMP_OFF.
          4. If the pump is performing PUMP_IN and the height is above the
          target
             height, then the pump shall be turned to PUMP_OFF, otherwise
             the pump
             shall remain at PUMP_IN.
          5. If the pump is performing PUMP_OUT and the height is below
          the target
             height, then the pump shall be turned to PUMP_OFF, otherwise,
             the pump
             shall remain at PUMP_OUT.

        :param current_height: the current height of liquid in the tank
        :param current_action: the current action of the pump
        :param actions: a dictionary containing the keys 'PUMP_IN', 'PUMP_OFF',
                        and 'PUMP_OUT'
        :return: The new action for the pump: one of actions['PUMP_IN'],
        actions['PUMP_OUT'], actions['PUMP_OFF']
        """
        new_action = current_action
        if current_height < 0:
            raise Exception('Sensor reading cannot be less than 0.')
        if current_action not in (-1, 0, 1):
            logging.debug('In Decider, the pump status is %s', current_action)
            raise Exception('Bad Pump Status')

        if current_action == 0 and current_height < (self.target_height -
                                                     self.margin):
            logging.debug('In Decider, the value of current_height is %s',
                          current_height)
            logging.debug('In Decider, the value of current_action is %s',
                          current_action)
            logging.debug('In Decider, the value of target_height is %s',
                          self.target_height)
            logging.debug('In Decider, the return value is %s',
                          actions['PUMP_IN'])
            new_action = actions['PUMP_IN']

# If the pump is off and the height is above the margin region, then the
        # pump should be
# turned to PUMP_OUT.
        if current_action == 0 and current_height > (self.target_height +
                                                     self.margin):
            new_action = actions['PUMP_OUT']

# If the pump is off and the height is within the margin region or on
# the exact boundary of the margin region, then the pump shall remain at
        # PUMP_OFF
        if current_action == 0 and (self.target_height - self.margin) \
                <= current_height <= (self.target_height + self.margin):
            new_action = actions['PUMP_OFF']

# If the pump is performing PUMP_IN and the height is above the target
# height, then the pump shall be turned to PUMP_OFF, otherwise the pump shall
        # remain at PUMP_IN.
        if current_action == 1 and (self.target_height) < current_height:
            new_action = actions['PUMP_OFF']

# If the pump is performing PUMP_IN and the height is less than or equal to
        # target
# height plus margin, then the pump shall remain at PUMP_IN.
        if current_action == 1 and (self.target_height) >= current_height:
            new_action = actions['PUMP_IN']

# If the pump is performing PUMP_OUT and the height is below the target
        # height, then the pump shall
# be turned to PUMP_OFF, otherwise, the pump shall remain at PUMP_OUT

        if current_action == -1 and self.target_height > current_height:
            new_action = actions['PUMP_OFF']

        if current_action == -1 and self.target_height <= current_height:
            new_action = actions['PUMP_OUT']

        return new_action
