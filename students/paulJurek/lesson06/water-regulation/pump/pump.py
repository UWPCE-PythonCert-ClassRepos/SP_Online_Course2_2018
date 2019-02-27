"""
Encapsulates the connection to an HTTP pump controller.
"""

import urllib.request
import urllib.error


class Pump(object):
    """
    Encapsulates the connection to an HTTP pump controller
    """

    PUMP_IN = 1
    PUMP_OFF = 0
    PUMP_OUT = -1
    actions_str_2_int = {'PUMP_IN': 1,
                         'PUMP_OFF': 0,
                         'PUMP_OUT': -1}
    actions_int_2_str = {1: 'PUMP_IN',
                         0: 'PUMP_OFF',
                         -1: 'PUMP_OUT'}

    def __init__(self, address, port):
        """
        Create a connection to a pump controller.

        :param address: the address of the pump controller
        :param port: the port number of the pump controller
        """

        self.address = address
        self.port = port

    def set_state(self, state: str) -> bool:
        """
        Set the state of the remote pump.

        :param state: One of PUMP_IN, PUMP_OFF, PUMP_OUT
        :return: True if the remote pump controller acknowledges the request,
            otherwise False
        """
        state_int = self.actions_str_2_int[state]

        request = urllib.request.Request(self.address + ':' + self.port,
                                         state_int)

        try:
            urllib.request.urlopen(request)
        except urllib.error.HTTPError:
            return False

        return True

    def get_state(self) -> str:
        """
        Get the state of the remote pump.

        :return: int representing one of PUMP_IN, PUMP_OFF, PUMP_OUT
        """
        response = urllib.request.urlopen(self.address + ":" + self.port)
        return self.actions_int_2_str[int(response.read)]

    def PUMP_IN(self):
        """interface to call set_state for turning pump in"""
        return self.set_state(state='PUMP_IN')

    def PUMP_OFF(self):
        """interface to call set_state for turning pump off"""
        return self.set_state(state='PUMP_OFF')

    def PUMP_OUT(self):
        """interface to call set_state for turning pump out"""
        return self.set_state(state='PUMP_OUT')
