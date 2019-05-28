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
link2 = 'https://steamcommunity.com/market/listings/730/Gamma%20Case%20Key'
link3 = 'https://www.rmf24.pl/fakty/swiat/news-niesamowite-zdjecie-orla-zachwyca-sie-nim-caly-swiat,nId,3014481'

r = grab_web(link3)
thisSoup = bs4.BeautifulSoup(r.content, "lxml")  # as ebook says r.text !
# print(thisSoup)

results = thisSoup.find_all(attrs='article-title')
# results = thisSoup.findAll("div", {"class": "entry-title"})

for element in results:
    print(element.getText())
# price_sell_table = thisSoup.select('#market_commodity_forsale_table')
# table = thisSoup.find(lambda tag: tag.name=='market_commodity_forsale_table' and tag.has_attr('id') and tag['id']=="market_commodity_forsale_table")
# rows = table.findAll(lambda tag: tag.name=='tr')


''' Writing results to file'''
# with open('web.txt', 'w') as file:
#     # res = re.match(r'((src)|(href))="(.*png)"',html)
#     # file.write(html)
#
#     # print(res)
#     pass
    

print('Done!')