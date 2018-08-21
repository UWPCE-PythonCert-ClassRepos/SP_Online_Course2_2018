"""
Encapsulates decision making in the water-regulation module
"""


class Decider(object):
    """
    Encapsulates decision making in the water-regulation module
    """

    def __init__(self, target_height, margin):
        """
        Create a new decider instance for this tank.

        :param target_height: the target height for liquid in this tank
        :param margin: the margin of liquid above and below the target
                        height for which the pump should not turn on.
                        Ex: .05 represents a 5% margin above and below
                        the target_height.
        """
        self.target_height = target_height
        self.margin = margin
        deadband = target_height * margin
        self.lower_limit = target_height - deadband
        self.upper_limit = target_height + deadband

    def pump_is_in(self, current_height, actions):
        '''
        4. If the pump is performing PUMP_IN and the height is above the
            target height, then the pump shall be turned to PUMP_OFF,
            otherwise the pump shall remain at PUMP_IN.
        '''
        action = 'PUMP_IN'
        if current_height > self.target_height:
            action = 'PUMP_OFF'
        return actions[action]

    def pump_is_out(self, current_height, actions):
        '''
          5. If the pump is performing PUMP_OUT and the height is below the
            target height, then the pump shall be turned to PUMP_OFF,
            otherwise, the pump shall remain at PUMP_OUT.
        '''
        action = 'PUMP_OUT'
        if current_height < self.target_height:
            action = 'PUMP_OFF'
        return actions[action]

    def pump_is_off(self, current_height, actions):
        '''
          1. If the pump is off and the height is below the margin region,
            then the pump should be turned to PUMP_IN.
          2. If the pump is off and the height is above the margin region,
            then the pump should be turned to PUMP_OUT.
          3. If the pump is off and the height is within the margin region
            or on the exact boundary of the margin region, then the pump
            shall remain at PUMP_OFF.
        '''
        action = 'PUMP_OFF'
        if current_height < self.lower_limit:
            action = 'PUMP_IN'
        elif current_height > self.upper_limit:
            action = 'PUMP_OUT'
        return actions[action]

    def decide(self, current_height, current_action, actions):
        """
        Decide a new action for the pump, given the current height of liquid
        in the tank and the current action of the pump.

        Note that the new action for the pump MAY be the same as the current
        action of the pump.

        The *decide* method shall obey the following behaviors:

          1. If the pump is off and the height is below the margin region,
            then the pump should be turned to PUMP_IN.
          2. If the pump is off and the height is above the margin region,
            then the pump should be turned to PUMP_OUT.
          3. If the pump is off and the height is within the margin region
            or on the exact boundary of the margin region, then the pump
            shall remain at PUMP_OFF.
          4. If the pump is performing PUMP_IN and the height is above the
            target height, then the pump shall be turned to PUMP_OFF,
            otherwise the pump shall remain at PUMP_IN.
          5. If the pump is performing PUMP_OUT and the height is below the
            target height, then the pump shall be turned to PUMP_OFF,
            otherwise, the pump shall remain at PUMP_OUT.

        :param current_height: the current height of liquid in the tank
        :param current_action: the current action of the pump
        :param actions: a dictionary containing the keys 'PUMP_IN', 'PUMP_OFF',
                        and 'PUMP_OUT'
        :return: The new action for the pump:
            one of actions['PUMP_IN'], actions['PUMP_OUT'], actions['PUMP_OFF']
        """

        # Next action depends first on the pump state
        # Create a dict of actions (like a switch statement)
        action_choices = {
            'PUMP_IN': self.pump_is_in,
            'PUMP_OUT': self.pump_is_out,
            'PUMP_OFF': self.pump_is_off
        }

        return action_choices[current_action](current_height, actions)
