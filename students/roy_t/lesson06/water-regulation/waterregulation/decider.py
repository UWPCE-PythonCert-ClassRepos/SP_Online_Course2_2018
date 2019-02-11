"""
Encapsulates decision making in the water-regulation module
"""


class Decider:
    """
    Encapsulates decision making in the water-regulation module
    """

    def __init__(self, target_height, margin):
        """
        Create a new decider instance for this tank.

        :param target_height: the target height for liquid in this tank
        :param margin: the margin. 0.05 = 5%
        """
        self.target_height = target_height
        self.margin = margin

    def decide(self, cur_height, cur_action, actions):
        """
        Make a decision based on the parameters provided.

        NOTE: The resulting action may be 'no action needed'

        The *decide* method shall obey the following behaviors:

          1. If the pump is off and the height is below the margin region,
          then the pump should be turned to PUMP_IN.
          2. If the pump is off and the height is above the margin region,
          then the pump should be turned to PUMP_OUT.
          3. If the pump is off and the height is within the margin region
          or on the exact boundary of the margin region, then the pump shall
           remain at PUMP_OFF.
          4. If the pump is performing PUMP_IN and the height is above the
          target height, then the pump shall be turned to PUMP_OFF,
          otherwise the pump shall remain at PUMP_IN.
          5. If the pump is performing PUMP_OUT and the height is below
          the target  height, then the pump shall be turned to PUMP_OFF,
          otherwise, the pump shall remain at PUMP_OUT.

        :param cur_height: the current height of liquid in the tank
        :param cur_action: the current action of the pump
        :param actions: a dictionary containing the keys 'PUMP_IN',
        'PUMP_OFF', and 'PUMP_OUT'
        :return: The new action for the pump: one of actions['PUMP_IN'],
        actions['PUMP_OUT'], actions['PUMP_OFF']
        """
        cur_margin = (cur_height - self.target_height) / self.target_height
        if cur_action == actions['PUMP_OFF'] and cur_margin < self.margin:
            return actions['PUMP_IN']
        if cur_action == actions['PUMP_OFF'] and cur_margin > self.margin:
            return actions['PUMP_OUT']
        if cur_action == actions['PUMP_OFF'] and cur_margin <= self.margin:
            return actions['PUMP_OFF']
        if cur_action == actions['PUMP_IN'] and \
                cur_height > self.target_height:
            return actions['PUMP_OFF']
        if cur_action == actions['PUMP_IN'] and \
                cur_height <= self.target_height:
            return actions['PUMP_IN']
        if cur_action == actions['PUMP_OUT'] and \
                cur_height < self.target_height:
            action = actions['PUMP_OFF']
        else:
            action = actions['PUMP_OUT']
        return action
