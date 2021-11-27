#` -*- coding: utf-8 -*-

import spotipy
import spotipy.util as util
import time
import sys
import textwrap

from PIL import ImageFont

from demo_opts import get_device
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator



import multiprocessing


import logging

logging.disable(logging.CRITICAL)



trackQueue = multiprocessing.Queue()






def spotifyAPIPull():

    scope = 'user-read-currently-playing'
    token = util.prompt_for_user_token(12173622847, scope, client_id='7b7b8b48cb6d45a89e18a4e7684ee8fc', client_secret='0a825bd502344d9ca6e5afe9c4bf2101', redirect_uri="http://localhost:8888/callback")
    spotify = spotipy.Spotify(auth=token)
    while True:
            current_track = spotify.current_user_playing_track()['item']['name']
            trackQueue.put(current_track)
            time.sleep(1)



def screenDraw():

    currentlyDisplayed=''
    device = get_device()


    while True:
        songNameUpdate=trackQueue.get()

        if songNameUpdate != currentlyDisplayed:
            currentlyDisplayed = songNameUpdate
            fontsize=1
            
            font = ImageFont.truetype("Noto.otf", fontsize)

            lines = textwrap.wrap(currentlyDisplayed, width=15)
            lines.reverse()



            longestLine=lines[0]
            for line in lines:
                if font.getsize(line)[1] > font.getsize(longestLine)[0]:
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

            

         


if __name__ == '__main__':
    spotifyProc = multiprocessing.Process(target=spotifyAPIPull, args=())
    screenProc = multiprocessing.Process(target=screenDraw, args=())

    spotifyProc.start()
    screenProc.start()