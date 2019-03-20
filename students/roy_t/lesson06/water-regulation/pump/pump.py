"""
Encapsulates the connection to an HTTP pump controller.
"""

import urllib.request
import urllib.error


class Pump:
    """
    Encapsulates the connection to an HTTP pump controller
    """

    PUMP_IN = 1
    PUMP_OFF = 0
    PUMP_OUT = -1

    def __init__(self, address, port):
        """
        Create a connection to a pump controller.

        :param address: the address of the pump controller
        :param port: the port number of the pump controller
        """

        self.address = address
        self.port = port

    def set_state(self, state):
        """
        Set the state of the remote pump.

        :param state: One of PUMP_IN, PUMP_OFF, PUMP_OUT
        :return: True if the remote pump controller acknowledges the request, otherwise False
        """

        request = urllib.request.Request(self.address + ':' + self.port, state)

        try:
            urllib.request.urlopen(request)
        except urllib.error.HTTPError:
            return False

        return True

    def get_state(self):
        """
        Get the state of the remote pump.

        :return: One of PUMP_IN, PUMP_OFF, PUMP_OUT
        """
        response = urllib.request.urlopen(self.address + ":" + self.port)
        return int(response.read)
