# -*- coding: utf-8 -*-

#Created on Fri Jun 22 12:46:21 2018


# A small system log server in python that prints any
# incoming messages.
#
# This can accept input from either a SysLogHandler or a
# UDPHandler, but output from a UDPHandler will be very
# ugly.

# Derived from https://gist.github.com/marcelom/4218010


HOST, PORT = "0.0.0.0", 514


import socketserver


class SyslogUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        try:
            data = data.decode()
        except UnicodeDecodeError:
            # The message was sent by a UDPHandler. It will be ugly.
            pass
        socket = self.request[1]
        print( "%s : " % self.client_address[0], str(data))

if __name__ == "__main__":
    try:
        server = socketserver.UDPServer((HOST,PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")