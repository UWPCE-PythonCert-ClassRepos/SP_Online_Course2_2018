"""
Encapsulates decision making in the water-regulation module
"""


# pylint: disable = too-few-public-methods
class Decider():
    """
    Encapsulates decision making in the water-regulation module
    """

    def __init__(self, target_height, margin):
        """
        Create a new decider instance for this tank.

        :param target_height: the target height for liquid in this tank
        :param margin: the margin of liquid above and below the target height
                     for which the pump should not turn on. Ex: .05
                     represents a 5% margin above and below the target_height.
        """
        self.target_height = target_height
        self.margin = margin

    def decide(self, current_height, current_action, actions):
        """
        Decide a new action for the pump, given the current height of liquid
        in the tank and the current action of the pump.
        """
        if current_action == "PUMP_OFF":
            if current_height < self.target_height - (self.target_height *
                                                      self.margin):
                action_change = "PUMP_IN"
            elif current_height > self.target_height + (self.target_height *
                                                        self.margin):
                action_change = "PUMP_OUT"
            else:
                action_change = "PUMP_OFF"
        if current_action == "PUMP_IN":
            if current_height > self.target_height:
                action_change = "PUMP_OFF"
            else:
                action_change = "PUMP_IN"
        if current_action == "PUMP_OUT":
            if current_height < self.target_height:
                action_change = "PUMP_OFF"
            else:
                action_change = "PUMP_OUT"
        return actions[action_change]
