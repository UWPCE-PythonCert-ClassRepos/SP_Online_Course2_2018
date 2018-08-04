"""
Encapsulates decide making in the water-regulation module
"""


class Decider(object):
    """
    Encapsulates decide making in the water-regulation module
    """

    def __init__(self, target_height, margin):
        """
        Create a new decider instance for this tank.

        :param target_height: the target height for liquid in this tank
        :param margin: the margin of liquid above and below the target \
height for
                       which the pump should not turn on. Ex: .05 represents a
                       5% margin above and below the target_height.
        """
        self.target_height = target_height
        self.margin = margin

    def decide(self, current_height, current_action, actions):
        """
        Make Decisions
        """

        new_action = current_action

        if current_action == actions['PUMP_OFF']:
            if current_height < self.target_height - self.target_height * \
                    self.margin:
                new_action = actions['PUMP_IN']
            elif current_height > self.target_height + self.target_height * \
                    self.margin:
                new_action = actions['PUMP_OUT']
            else:
                new_action = actions['PUMP_OFF']
        if current_action == actions['PUMP_IN']:
            if current_height > self.target_height:
                new_action = actions['PUMP_OFF']
            else:
                new_action = actions['PUMP_IN']
        if current_action == actions['PUMP_OUT']:
            if current_height < self.target_height:
                new_action = actions['PUMP_OFF']
            else:
                new_action = actions['PUMP_OUT']
        return new_action
