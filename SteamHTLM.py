import numpy as np
import shutil
import os
import re
import json
import requests
import bs4
from SteamMarketAPI import grab_image

def download_pictures():
    results = thisSoup.find_all("img", src=re.compile("((https)|(www)).*((\.bmp)|(\.jpg)|(\.png))$"))
    for element in results:
        new_url = element.get('src')
        name = os.path.basename(new_url)

        this_image = grab_image(new_url)
        width, height = this_image.size
        if width > 150 and height > 150:
            with open('pics\\' + name, 'wb') as file:
                this_image.save(file)
                print('Saved picture:', file.name)


def download_a_pictures():
    results = thisSoup.find_all("a")
    for element in results:
        # new_url = element.get('src')

        for child in element.children:
            if type(child) == bs4.element.Tag:
                if child.get('src'):
                    new_url = child.get('src')
                    name = os.path.basename(new_url)
                    name = name.replace('?', '')

                    this_image = grab_image(new_url)
                    width, height = this_image.size

                    if width > 150 and height > 150:
                        this_type = name[-3:]
                        if not('png' in this_type or 'bmp' in this_type or 'jpg' in this_type or 'png' in this_type):
                            name += '.png'

                        with open('pics\\' + name, 'wb') as file:
                            this_image.save(file)
                            print('Saved picture:', file.name)


def grab_title(soup):
    # Compatible with RMF24 Web Page
    results = soup.find_all(attrs='article-title')
    return results


def grab_web(url):
    req = requests.get(url, stream=True)
    req.raise_for_status()
    req.raw.decode_content = True
    return req


link_market = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730'
link2 = 'https://steamcommunity.com/market/listings/730/Gamma%20Case%20Key'
link3 = 'https://memy.jeja.pl/'

r = grab_web(link3)
thisSoup = bs4.BeautifulSoup(r.text, "html.parser")  # as ebook says r.text !

download_pictures()
download_a_pictures()


# price_sell_table = thisSoup.select('#market_commodity_forsale_table')
# table = thisSoup.find(lambda tag: tag.name=='market_commodity_forsale_table' and tag.has_attr('id') and tag['id']=="market_commodity_forsale_table")
# rows = table.findAll(lambda tag: tag.name=='tr')



print('Done!')