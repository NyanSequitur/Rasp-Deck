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


ev = volumeTest.IAudioEndpointVolume.get_default()
vol = ev.GetMasterVolumeLevelScalar()
vmin, vmax, vinc = ev.GetVolumeRange()

muteStatus = True
searching = True
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))		
print ("socket binded to %s" %(port))
s.listen(5)

while True:
    # put the socket into listening mode
    
    print ("socket is listening")		

    # a forever loop until we interrupt it or
    # an error occurs
    c, addr = s.accept()
    print ('Got connection from', addr )

    searching = False


    while searching == False:

    # Establish connection with client.
    

        dataFromClient = c.recv(1024)
        decodedData = dataFromClient.decode()


        if decodedData == 'u':
            ev.VolumeStepUp()
        elif decodedData == 'd':
            ev.VolumeStepDown()
        elif decodedData == 'm':
            if muteStatus:
                ev.SetMute(False)
            else:
                ev.SetMute(True)
            muteStatus = not muteStatus
        elif decodedData == 'exit':
            searching = True
