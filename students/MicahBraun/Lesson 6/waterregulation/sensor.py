"""
AUTHOR: Instrucor
PROJECT NAME: sensor.py
DATE CREATED: 10/19/2018
UPDATED: 10/22/2018
PURPOSE: Lesson 6
DESCRIPTION: File provides a sensor proxy to gather
data from.
"""
import urllib.request


class Sensor:
    """
    Encapsulates the connection to an HTTP liquid height sensor controller
    """

    def __init__(self, address, port):
        """
        Create a connection to a liquid height sensor controller.
        """
        self.address = address
        self.port = port

    def measure(self):
        """
        Set the state of the remote liquid height sensor.
        """
        response = urllib.request.urlopen(self.address + ":" + self.port)
        return float(response.read)
