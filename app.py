from flask import Flask, render_template
import textwrap, multiprocessing, logging, spotipy, time, textwrap, os
import spotipy.util as util
from PIL import ImageFont
from demo_opts import get_device
from luma.core.render import canvas
from pathlib import Path
from datetime import datetime
import psutil

trackQueue = multiprocessing.Queue()

logging.disable(logging.CRITICAL)

app = Flask(__name__)

trackQueue = multiprocessing.Queue()

modeQueue = multiprocessing.Queue()































# SPOTIFY FUNCTION


def spotifyAPIPull():

    scope = 'user-read-currently-playing user-read-recently-played'
    token = util.prompt_for_user_token(12173622847, scope, client_id='7b7b8b48cb6d45a89e18a4e7684ee8fc', client_secret='0a825bd502344d9ca6e5afe9c4bf2101', redirect_uri="http://localhost:8888/callback")
    spotify = spotipy.Spotify(auth=token)
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
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n


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
    # use custom font
    
    font2 = ImageFont.truetype('Noto.otf', 10)

    with canvas(device) as draw:
        draw.text((0, 0), cpu_usage(), font=font2, fill="white")
        if device.height >= 32:
            draw.text((0, 14), mem_usage(), font=font2, fill="white")

        if device.height >= 64:
            draw.text((0, 26), disk_usage('/'), font=font2, fill="white")
            try:
                draw.text((0, 38), network('wlan0'), font=font2, fill="white")
            except KeyError:
                # no wifi enabled/available
                pass

















































































def screenDraw():
    currentlyDisplayed=''
    forceUpdate=False

    mode = modeQueue.get()
    device = get_device()
    while True:
        if not modeQueue.empty():
            mode = modeQueue.get()
            forceUpdate=True
        print(mode)
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


if __name__ == '__main__':

    spotifyProc = multiprocessing.Process(target=spotifyAPIPull, args=())
    screenProc = multiprocessing.Process(target=screenDraw, args=())
    spotifyProc.start()
    screenProc.start()

    app.run(debug=True,host="0.0.0.0",port=5000,use_reloader=False)