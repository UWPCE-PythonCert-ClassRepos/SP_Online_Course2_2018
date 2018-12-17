"""
Encapsulates decision making in the water-regulation module
"""


class Decider():
    """
    Encapsulates decision making in the water-regulation module
    """

    def __init__(self, target_height, margin):
        """
        Create a new decider instance for this tank.

        :param target_height: the target height for liquid in this tank
        :param margin: the margin of liquid above and below the target height for
                       which the pump should not turn on. Ex: .05 represents a
                       5% margin above and below the target_height.
        """
        self.target_height = target_height
        self.margin = margin
        self.upper = target_height + margin
        self.lower = target_height - margin


    def height_checker(self, cur_height):
        """
        Checks current height to target height
        returns int whether current height is below, between, or above target height
        """

        above = 2
        good = 1
        below = 0

        if cur_height < self.lower:
            return below
        if cur_height > self.upper:
            return above
        return good

    @staticmethod
    def decide_pump_action(current_action, actions):
        """
        Closer function that returns an action based on the current status of pump and water level.
        """

        def decide_level(current_height):
       
            if current_action == -1:
                if current_height == 0:
                    return actions['PUMP_OFF']#PUMP_OUT and below
                return actions['PUMP_OUT'] #PUMP_OUT and in between or level or above level
            if current_action == 0:      
                if current_height == 0:
                    return actions['PUMP_IN']#PUMP_OFF and below
                if current_height == 2:
                    return actions['PUMP_OUT'] #PUMP_OFF and above level
                return actions['PUMP_OFF'] #PUMP_OFF and in between level
            if current_action == 1:
                if current_height == 2:
                    return actions['PUMP_OFF']#PUMP_IN and above
                return actions['PUMP_IN'] #PUMP_IN and either in between level or below min level

        return decide_level
