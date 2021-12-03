#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import random
import time


s = socket.socket()         # Create a socket object
host = '169.254.61.140'
port = 12345                # Reserve a port for your service.

s.connect((host, port))
while True:
    s.send('up'.encode())
    time.sleep(.5)