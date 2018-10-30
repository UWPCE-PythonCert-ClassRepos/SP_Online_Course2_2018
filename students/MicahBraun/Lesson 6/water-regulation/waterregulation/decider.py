"""
AUTHOR: Micah Braun
PROJECT NAME: decider.py
DATE CREATED: 10/19/2018
LAST-UPDATED: 10/29/2018
PURPOSE: Lesson 6
DESCRIPTION: File provides the 'brain' for the pump,
dictating when and under what conditions to change
state.
"""


class Decider:
    """
    Encapsulates decision making in the water-regulation module
    """
    def __init__(self, target_height, margin):
        """
        Create a new decider instance for this tank.
        height for which the pump should not turn on. Ex: .05 represents
        a 5% margin above and below the target_height.
        """
        self.target_height = target_height
        self.margin = margin

    def decide(self, current_height, current_state, actions):
        """
        Decide a new action for the pump, given the current height of
        liquid in the tank and the current action of the pump.
        Note that the new action for the pump MAY be the same as the
        current action of the pump.
        1: pump_off, liquid_down == PUMP_IN
        2: pump_off, liquid_up == PUMP_OUT
        3: pump_off, liquid_mid == PUMP_OFF -- state does not change
        4: PUMP_IN, liquid_up == PUMP_OFF, else no change
        5: PUMP_OUT, liquid_down == PUMP_OFF, else no change
        """
        new_state = current_state
        # Conditions for Pump states:
        if current_state == actions['PUMP_OFF']:
            if current_height < self.target_height - \
                    self.target_height * self.margin:
                new_state = actions['PUMP_IN']
            elif current_height > self.target_height + \
                    self.target_height * self.margin:
                new_state = actions['PUMP_OUT']
            else:
                new_state = current_state
        if current_state == actions['PUMP_IN']:
            if current_height > self.target_height:
                new_state = actions['PUMP_OFF']
            else:
                new_state = current_state
        if current_state == actions['PUMP_OUT']:
            if current_height < self.target_height:
                new_state = actions['PUMP_OFF']
            else:
                new_state = current_state
        return new_state
