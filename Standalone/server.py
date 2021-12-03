# first of all import the socket library
import socket			
import volumeTest
import random

# next create a socket object
s = socket.socket()		
print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345			

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))		
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)	
print ("socket is listening")		

ev = volumeTest.IAudioEndpointVolume.get_default()
vol = ev.GetMasterVolumeLevelScalar()
vmin, vmax, vinc = ev.GetVolumeRange()




# a forever loop until we interrupt it or
# an error occurs
c, addr = s.accept()
print ('Got connection from', addr )

while True:

# Establish connection with client.
    

    dataFromClient = c.recv(1024)

    if dataFromClient.decode() == 'up':
        ev.VolumeStepUp()
        print('up')
    elif dataFromClient.decode == 'down':
        ev.VolumeStepDown()
        print('down')
