import numpy as np
#import steam
import shutil
import os

from PIL import Image
import matplotlib.pyplot as plt
import json
import requests

cat_link = r'https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fimages.wisegeek.com%2Fyoung-calico-cat.jpg&f=1'

def grab_image(url):
    req = requests.get(url, stream=True)
    if req.status_code == 200:
        req.raw.decode_content = True
        img = Image.open(req.raw)
        return img
    else:
        raise BaseException

""" Saving picture on disk. Loop breaks showing afterwads"""

cat_img = grab_image(cat_link)
file_pic = open('cat.png', 'wb')
cat_img.save(file_pic)
file_pic.close()

plt.imshow(cat_img)  # Ploting
# plt.show()


res = requests.get('https://automatetheboringstuff.com/files/rj.txt')
res.raise_for_status()
playFile = open('RomeoAndJuliet.txt', 'wb')
for chunk in res.iter_content(100000):
    playFile.write(chunk)
playFile.close()