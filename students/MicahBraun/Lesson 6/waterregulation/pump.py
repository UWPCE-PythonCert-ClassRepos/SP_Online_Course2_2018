"""
FROM: Original file given by Instructor
AUTHOR: Micah Braun
PROJECT NAME: pump.py
DATE CREATED: 10/19/2018
UPDATED: 10/22/2018
PURPOSE: Lesson 6
DESCRIPTION: Pump class relays pump behavior (get and
set state modules for waterregulation package).
"""
import urllib.request
import urllib.error


class Pump:
    """
    Encapsulates the connection to an HTTP pump controller
    """
    PUMP_IN = 1
    PUMP_OUT = -1
    PUMP_OFF = 0

    def __init__(self, address, port):
        """
        Create a connection to a pump controller.
        """
        self.address = address
        self.port = port

    def set_state(self, state):
        """
        Set the state of the remote pump.
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
        """
        response = urllib.request.urlopen(self.address + ":" + self.port)
        return int(response.read)
