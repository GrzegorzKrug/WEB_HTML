import numpy as np
import shutil
import os
import re
import json
import requests
import bs4


def grab_web(url):
    req = requests.get(url, stream=True)
    req.raise_for_status()
    req.raw.decode_content = True
    return req

link = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730'

html = ''
r = grab_web(link)
for chunk in r:
    html += str(chunk)

with open('web.txt', 'w') as file:
    res = re.match(r'((src)|(href))="(.*png)"',html)

##    print(html[:1000])
    print(res)
    
    

