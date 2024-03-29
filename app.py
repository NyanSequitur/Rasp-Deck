from flask import Flask, render_template
import textwrap, multiprocessing, logging, spotipy, time, textwrap, os, socket, psutil, atexit, signal
import spotipy.util as util
from PIL import ImageFont
from demo_opts import get_device
from luma.core.render import canvas
from pathlib import Path
from datetime import datetime
import RPi.GPIO as GPIO



from encoder import Encoder

import keyOutput
import subprocess

trackQueue = multiprocessing.Queue()

logging.disable(logging.CRITICAL)

app = Flask(__name__)

trackQueue = multiprocessing.Queue()

modeQueue = multiprocessing.Queue()

socketPass = multiprocessing.Queue()



scope = 'user-read-currently-playing user-read-recently-played user-modify-playback-state user-read-playback-state'
   
token = util.prompt_for_user_token(12173622847, scope, client_id='', client_secret='', redirect_uri="http://localhost:8888/callback")

spotify = spotipy.Spotify(auth=token)






def spotifyAPIPull(spotify):

    
    while True:
        
        try:
            current_track = spotify.current_user_playing_track()['item']['name']
        except TypeError:
            current_track = spotify.current_user_recently_played(1)['items'][0]['track']['name']
        trackQueue.put(current_track)
        time.sleep(1)

def spotifyDraw(device, currentlyDisplayed, forceUpdate):
    
    songNameUpdate=trackQueue.get()

    if songNameUpdate != currentlyDisplayed or forceUpdate:
        currentlyDisplayed = songNameUpdate
        fontsize=1
            
        font = ImageFont.truetype("Noto.otf", fontsize)

        lines = textwrap.wrap(currentlyDisplayed, width=15)
        lines.reverse()

        longestLine=lines[0]
        for line in lines:
            if font.getsize(line)[0] > font.getsize(longestLine)[0]:
                longestLine = line

        while font.getsize(currentlyDisplayed)[1] < 64/len(lines) and font.getsize(longestLine)[0] < 128:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            font = ImageFont.truetype("Noto.otf", fontsize)

        fontsize -= 1
        font = ImageFont.truetype("Noto.otf", fontsize)

            


        with canvas(device) as draw:
            w, h = draw.textsize(text=currentlyDisplayed, font=font)
            y_text = h
            for line in lines:
                width, height = font.getsize(line)
                draw.text(((0), (device.height - y_text)), line, font=font, fill="white")
                y_text += h
    return currentlyDisplayed
















def bytes2human(n):

    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n



def getIP():
    return subprocess.check_output("hostname -I | cut -d\' \' -f1", shell = True )


def cpu_usage():
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f Up: %s" \
        % (av1, av2, av3, str(uptime).split('.')[0])


def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
        % (bytes2human(usage.used), usage.percent)


def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))


def stats(device):
    
    font2 = ImageFont.truetype('Noto.otf', 10)

    with canvas(device) as draw:
        draw.text((0, 0), cpu_usage(), font=font2, fill="white")
        draw.text((0, 14), mem_usage(), font=font2, fill="white")

        draw.text((0, 26), disk_usage('/'), font=font2, fill="white")
        draw.text((0, 38), str(getIP(), 'utf-8'), font=font2, fill="white")









            


def keySwitchFunc(spotify):




    
    pinList=[[26,19,13,16],[6,5],[],[14]]
    
    keyOutput.pinSetup(pinList)
    pressedStatus=[]

    tempList=[]

    for mode in pinList:
        for pin in mode:
            tempList.append(True)
        pressedStatus.append(tempList)
        tempList=[]





    
    position = 0
    spotifyStatus=False
    privateWindowStatus=False
    
    while True:

        funcList=[[spotify.next_track,''], [spotify.previous_track,'']]
        switchFuncList=[]
        # keystroke macros

        for pin in pinList[0]:
            position = pinList[0].index(pin)
            pressedStatus[0][position]=keyOutput.macroButton(pin,'key'+str(position+1)+'.csv',pressedStatus[0][position])
            

        # function macros

        for pin in pinList[1]:
            position = pinList[1].index(pin)
            pressedStatus[1][position]=keyOutput.funcMacroButton(pin,pressedStatus[1][position],funcList[position][0],funcList[position][1])
        
        # two-function switches

        for pin in pinList[2]:
            position = pinList[2].index(pin)
        
        keyOutput.pinSetupDown([[20]])

        privateWindowStatus = keyOutput.twoTextSwitch(20,privateWindowStatus,[['lalt','f4']],[['windows'],'h','t','t','p','s',['lshift',';'],'/','/','g','o','o','g','l','e','.','c','o','m',['return']])
        spotifyStatus = keyOutput.spotifyToggle(14,spotifyStatus,spotify)
     


def volumeControl():
    keyOutput.pinSetupDown([[21]])
    

    volumeWheel = Encoder(15,18)
    
    currentValue = volumeWheel.getValue()
    updatedValue = currentValue

    s = socket.socket()         # Create a socket object
    host = '10.245.97.39'
    port = 12345                # Reserve a port for your service.


    socketPass.put(s)

    s.connect((host, port))

    muteStatus=True



    while True:
        updatedValue = volumeWheel.getValue()
        if currentValue != updatedValue:
            if currentValue < updatedValue:
                s.send('d'.encode())
            else:
                s.send('u'.encode())
        currentValue = updatedValue        
        muteStatus=keyOutput.oneFuncSwitch(21,muteStatus,sendMessage,(s,'m'))
        

def sendMessage(s, message):
    s.send(message.encode())


def screenDraw():
    currentlyDisplayed=''
    forceUpdate=False

    mode = modeQueue.get()
    device = get_device()
    onToggle = True


    while True:
        if not modeQueue.empty():
            previousMode=mode
            mode = modeQueue.get()
            forceUpdate=True
        if mode == 'spotify':
            currentlyDisplayed = spotifyDraw(device, currentlyDisplayed, forceUpdate)
        if mode == 'pi_info':
            stats(device)
        forceUpdate=False

            


@app.route("/spotify", methods=["POST"])
def led_on_r():
    modeQueue.put('spotify')
    print("spotify button")
    return "ok"

@app.route("/pi_info", methods=["POST"])
def led_off_r():
    modeQueue.put('pi_info')
    print("pi button")
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return render_template("button.html", title="Button", name="Sam Clark")

def exit_handler(led):


    print("turning LED off")
    GPIO.output(led, GPIO.LOW)
    print("LED off")

    print("getting socket")
    s = socketPass.get()
    print("got socket")

    print("sending exit message")
    s.send('exit'.encode())

    print("closing socket")
    s.close()
    print("socket closed")

if __name__ == '__main__':
    led = 23
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.HIGH)

    
    spotifyProc = multiprocessing.Process(target=spotifyAPIPull, args=(spotify,))
    screenProc = multiprocessing.Process(target=screenDraw, args=())
    keySwitchProc=multiprocessing.Process(target=keySwitchFunc,args=(spotify,))
    volumeProc=multiprocessing.Process(target=volumeControl,args=())
    spotifyProc.start()
    keySwitchProc.start()
    screenProc.start()
    volumeProc.start()
    modeQueue.put('spotify')
    atexit.register(exit_handler,led)
    app.run(debug=True,host="0.0.0.0",port=5000,use_reloader=False)
