import numpy as np
#import steam
import shutil
import os

from PIL import Image
import matplotlib.pyplot as plt
import json
import requests

cat_link = r'https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fimages.wisegeek.com%2Fyoung-calico-cat.jpg&f=1'

cat_r = requests.get(cat_link, stream=True)
cat_img = Image.open(cat_r.raw)

""" Saving picture on disk. Loop breaks showing afterwads"""

picture = open('cat.png', 'wb')
# for chunk in cat:
cat_img.save(picture)
picture.close()

# cat.raw.decode_content = True
# cat.seek(0)  # Not working

cat_img.show()
plt.imshow(cat_img)
plt.show()


# image.show()

# os.remove('cat.png')