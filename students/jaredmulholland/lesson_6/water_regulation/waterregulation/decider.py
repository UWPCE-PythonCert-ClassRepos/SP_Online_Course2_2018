"""
Encapsulates decision making in the water-regulation module
"""


class Decider():
    """
    Encapsulates decision making in the water-regulation module
    """
    def __init__(self, target_height, margin):

        """create a new decider instance for this tank
        param target_height: the target height for liquid in this tank
        param margin: the margin of liquid above and below the target height
        for which the pump should not turn on

        ex. 0.05 represents a 5% margin below target height"""

        self.target_height = target_height
        self.margin = margin

    def decide(self, current_height, current_action, actions):
        """Decide a new action for the pump, given the current height
            of liquid in the
            tank and the current action of the pump.

            Note that the new action for the pump MAY be the same as the
            current action of the pump.

            The *decide* method shall obey the following behaviors:

            1. If the pump is off and the height is below the margin region,
            then the pump should be turned to PUMP_IN.
            2. If the pump is off and the height is above the margin region,
            then the pump should be turned to PUMP_OUT.
            3. If the pump is off and the height is within the margin region
            or on the exact boundary of the margin region, then the pump shall
            remain at PUMP_OFF.
            4. If the pump is performing PUMP_IN and the height is above
            the target height, then the pump shall be turned to PUMP_OFF,
            otherwise the pump shall remain at PUMP_IN.
            5. If the pump is performing PUMP_OUT and the height is below
            the target height, then the pump shall be turned to PUMP_OFF,
            otherwise, the pump shall remain at PUMP_OUT.

            :param current_height: the current height of liquid in the tank
            :param current_action: the current action of the pump
            :param actions: a dictionary containing the keys 'PUMP_IN',
            'PUMP_OFF', and 'PUMP_OUT'
            :return: The new action for the pump:
            one of actions['PUMP_IN'], actions['PUMP_OUT'], actions['PUMP_OFF']
            """

        margin_low = self.target_height * (1-self.margin)
        margin_high = self.target_height * (1+self.margin)

        # 1
        if (current_action == actions['PUMP_OFF'] and current_height < margin_low):
            new_action = actions['PUMP_IN']
        # 2
        elif (current_action == actions['PUMP_OFF'] and current_height > margin_high):
            new_action = actions['PUMP_OUT']
        # 3
        elif (current_action == actions['PUMP_OFF']
              and (margin_low <= current_height <= margin_high)):
            new_action = actions['PUMP_OFF']
        # 4
        elif current_action == actions['PUMP_IN']:
            if current_height > self.target_height:
                new_action = actions['PUMP_OFF']
            else:
                new_action = current_action
        # 5
        elif current_action == actions['PUMP_OUT']:
            if current_height < self.target_height:
                new_action = actions['PUMP_OFF']
            else:
                new_action = current_action

        return new_action
