"""
Encapsulates the connection to an HTTP liquid height sensor controller.
"""

import urllib.request


class Sensor(object):
    """
    Encapsulates the connection to an HTTP liquid height sensor controller
    """

    def __init__(self, address, port):
        """
        Create a connection to a liquid height sensor controller.

        :param address: the address of the liquid height sensor controller
        :param port: the port number of the liquid height sensor controller
        """

        self.address = address
        self.port = port

    def measure(self):
        """
        Set the state of the remote liquid height sensor.

        :return: True if the remote liquid height sensor controller acknowledges the request, otherwise False
        """
        response = urllib.request.urlopen(self.address + ":" + self.port)
        return float(response.read)