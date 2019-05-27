import numpy as np
#import steam
import shutil
import os
from PIL import Image
import json
import requests

cat_link = r'https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fimages.wisegeek.com%2Fyoung-calico-cat.jpg&f=1'

cat = requests.get(cat_link, stream=True)

""" Saving picture on disk """
# picture = open('cat.png', 'wb')
# for chunk in cat:
#     picture.write(chunk)
# picture.close()

# cat.raw.decode_content = True
# cat.seek(0)  # Not working
image = Image.open(cat.raw)
image.show()
# os.remove('cat.png')