import numpy as np
#import steam
import shutil
import os

from PIL import Image
import matplotlib.pyplot as plt
import json
import requests
#test
cat_link = r'https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fimages.wisegeek.com%2Fyoung-calico-cat.jpg&f=1'

def grab_image(url):
    req = requests.get(url, stream=True)
    if req.status_code == 200:
        req.raw.decode_content = True
        img = Image.open(req.raw)
        return img
    else:
        raise BaseException

def read_key():
    ''' Reading from text file, put key only!'''
    file = open('steam_key.txt')
    steam_key =file.read().split()[0]  # Spliting to avoid new lines in text file
    return steam_key

steam_key = read_key()

''' Grabbing image'''
cat_img = grab_image(cat_link)
''' Saving File'''
file_pic = open('cat.png', 'wb')
cat_img.save(file_pic)
file_pic.close()

plt.imshow(cat_img)  # Ploting
# plt.show()

''' Grabbing Text '''
res = requests.get('https://automatetheboringstuff.com/files/rj.txt')
res.raise_for_status()
playFile = open('RomeoAndJuliet.txt', 'wb')
for chunk in res:
    playFile.write(chunk)
playFile.close()
