import numpy as np
import shutil
import os
import re
import json
import requests
import bs4
from SteamMarketAPI import grab_image

class FindNews():
    def __init__(self):
        self.duckduck_search = 'https://duckduckgo.com/?q='

    def get_items_by_key(self, soup, *keys, excact_len=False):
        # Grabing items from google
        #
        key_n = len(keys)
        this_keys = [key.split() for key in keys]
        results = soup.find_all('a')

        items_out = []
        for element in results:
            my_tuple = []

            for child in element.children:
                try:
                    url = element['href']
                    # print(str(url))
                except KeyError:
                    url = 'Not Found in element'
                # except TypeError:
                #     pass
                if type(child) == bs4.element.Tag:
                    try:
                        abc = [child.text for key in this_keys if child['class'] == key]
                        # if child['class'] == google_title.split() or child['class'] == google_adres.split():
                        if abc != []:
                            my_tuple.append(abc)
                        # print(my_tuple)
                    except KeyError:
                        pass
                    pass
            # print(len(my_tuple), key_n)
            if (len(my_tuple) == key_n and excact_len) \
            or (len(my_tuple) >= 1 and not excact_len):
                my_tuple.append(url[7:])  # cuting prefix "/url?q="
                items_out.append(tuple(my_tuple))
        return items_out

    def search_in_google(self, soup):

        out = []
        google_title = 'BNeawe vvjwJb AP7Wnd'  # Title
        google_adres = 'BNeawe UPmit AP7Wnd'  # URL
        gazetapl = 'iUh30'

        items = self.get_items_by_key(soup, google_title)

        return out

    def search_web(self, query):
        url = self.duckduck_search + query
        url = 'https://duckduckgo.com/?q=usa&t=ffab&atb=v131-1&ia=news'
        url = 'https://www.google.com/search?source=hp&ei=Y3z9XKLfM5GOrwTjjK_wCA&q=wiadomo%C5%9Bci&oq=wiad&gs_l=psy-ab.3.0.0i67j0i131i67j0i131l5j0l3.197.1046..1492...0.0..0.144.571.0j5......0....1..gws-wiz.....0..35i39j35i39i19.r1K-4RCuSk8'


        req = requests.get(url, True)
        req.raise_for_status()
        req.raw.decode_content = True
        soup = bs4.BeautifulSoup(req.text, "html.parser")  # as ebook says r.text !
        return soup

    def start(self):
        query = 'wiadomosci'
        soup = self.search_web('None')
        yield

        result = self.search_in_google(soup)
        print(result)



# link_market = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730'
# link2 = 'https://steamcommunity.com/market/listings/730/Gamma%20Case%20Key'
# link3 = 'https://memy.jeja.pl/'

# thisSoup = bs4.BeautifulSoup(r.text, "html.parser")  # as ebook says r.text !

# price_sell_table = thisSoup.select('#market_commodity_forsale_table')
# table = thisSoup.find(lambda tag: tag.name=='market_commodity_forsale_table' and tag.has_attr('id') and tag['id']=="market_commodity_forsale_table")
# rows = table.findAll(lambda tag: tag.name=='tr')


app = FindNews()

for _ in app.start():
    pass

print('Done!')