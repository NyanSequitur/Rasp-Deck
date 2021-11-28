from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from demo_opts import get_device
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator

import glob

regulator = framerate_regulator(fps=29.97)

frames = []

device = get_device()

# 1+len(glob.glob('frames/*.png'))

for num in range(100):
    num+=1



    if num <= 9:
        im=Image.open('frames/bad_apple_00'+str(num)+'.png').resize((128,64),Image.ANTIALIAS)
        print('frames/bad_apple_00'+str(num)+'.png')
    elif num <= 99:
        im=Image.open('frames/bad_apple_0'+str(num)+'.png').resize((128,64),Image.ANTIALIAS)
        print('frames/bad_apple_0'+str(num)+'.png')
    else:
        im=Image.open('frames/bad_apple_'+str(num)+'.png').resize((128,64),Image.ANTIALIAS)
        print('frames/'+str(num)+'.png')
    frames.append(im)
    
    n=1

for frame in frames:
    with regulator:
            print("printing frame "+str(n))
            device.Draw(frame)
            n++
